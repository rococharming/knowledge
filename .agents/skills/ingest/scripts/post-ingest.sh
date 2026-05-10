#!/bin/bash
# Ingest 后执行的后处理脚本
# 用法: ./post-ingest.sh <领域路径>

DOMAIN_PATH="${1%/}"

if [ -z "$DOMAIN_PATH" ]; then
    echo "错误: 请提供领域路径"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

if [[ "$DOMAIN_PATH" != /* ]]; then
    DOMAIN_PATH="$REPO_ROOT/$DOMAIN_PATH"
fi

if [[ "$DOMAIN_PATH" == "$REPO_ROOT/"* ]]; then
    DOMAIN_REL="${DOMAIN_PATH#$REPO_ROOT/}"
else
    DOMAIN_REL="$(basename "$DOMAIN_PATH")"
fi

COLLECTION_NAME=""
if [ -f "$DOMAIN_PATH/CLAUDE.md" ]; then
    COLLECTION_NAME=$(awk -F'`' '/collection 名称/ { print $2; exit }' "$DOMAIN_PATH/CLAUDE.md")
fi

if [ -z "$COLLECTION_NAME" ]; then
    DOMAIN_SLUG=$(basename "$DOMAIN_PATH" | tr '[:upper:]' '[:lower:]')
    COLLECTION_NAME="knowledge-$DOMAIN_SLUG"
fi

echo "=== Ingest 后处理 ==="

# 1. 更新 qmd 索引（如果 qmd 可用）
if command -v qmd &> /dev/null; then
    cd "$REPO_ROOT"

    COLLECTION_EXISTS=$(qmd collection list 2>/dev/null | awk '{ print $1 }' | grep -Fx "$COLLECTION_NAME" || true)
    QMD_READY=1

    if [ -z "$COLLECTION_EXISTS" ]; then
        echo "创建 qmd collection: $COLLECTION_NAME -> ./$DOMAIN_REL/wiki"
        if ! qmd collection add "./$DOMAIN_REL/wiki" --name "$COLLECTION_NAME" --mask "**/*.md"; then
            echo "警告: qmd collection 创建失败，跳过索引更新"
            QMD_READY=0
        fi
    fi

    if [ "$QMD_READY" -eq 1 ]; then
        echo "更新 qmd 索引..."
        if qmd update; then
            PENDING=$(qmd status 2>/dev/null | awk '/Pending:/ { print $2; exit }')
            if [ -n "$PENDING" ] && [ "$PENDING" != "0" ]; then
                echo "提示: qmd 仍有 $PENDING 个文档需要 embedding；BM25 搜索可用，语义搜索会在 query 时按需执行 qmd embed。"
            fi
        else
            echo "警告: qmd update 失败，索引可能不是最新；query 时可重试 qmd update。"
        fi
    fi

else
    echo "qmd 未安装，跳过索引更新"
fi

# 2. 统计新增页面
echo ""
echo "=== 新增页面统计 ==="
find "$DOMAIN_PATH/wiki" -name "*.md" -newer "$DOMAIN_PATH/CLAUDE.md" -exec basename {} \; 2>/dev/null | head -20

# 3. 检查孤立页面（没有入链的页面）
echo ""
echo "=== 检查孤立页面 ==="
while IFS= read -r -d '' file; do
    BASENAME=$(basename "$file" .md)
    # 检查是否被其他页面引用
    REFS=$(
        {
            grep -r -F "[[$BASENAME]]" "$DOMAIN_PATH/wiki" --include="*.md"
            grep -r -F "[[$BASENAME|" "$DOMAIN_PATH/wiki" --include="*.md"
            grep -r -F "[[$BASENAME#" "$DOMAIN_PATH/wiki" --include="*.md"
        } 2>/dev/null | grep -v -F "$file" | wc -l
    )
    if [ "$REFS" -eq 0 ]; then
        echo "  孤立: $BASENAME"
    fi
done < <(find "$DOMAIN_PATH/wiki" -name "*.md" ! -name "index.md" ! -name "log.md" -print0)

echo ""
echo "后处理完成"
