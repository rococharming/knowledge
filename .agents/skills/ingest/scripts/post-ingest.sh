#!/bin/bash
# Ingest 后执行的后处理脚本
# 用法: ./post-ingest.sh <领域路径>

DOMAIN_PATH="$1"

if [ -z "$DOMAIN_PATH" ]; then
    echo "错误: 请提供领域路径"
    exit 1
fi

echo "=== Ingest 后处理 ==="

# 1. 更新 qmd 索引（如果 qmd 可用）
if command -v qmd &> /dev/null; then
    echo "更新 qmd 索引..."
    cd "$DOMAIN_PATH"
    qmd update
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
for file in $(find "$DOMAIN_PATH/wiki" -name "*.md" | grep -v "index.md" | grep -v "log.md"); do
    BASENAME=$(basename "$file" .md)
    # 检查是否被其他页面引用
    REFS=$(grep -r "\[\[$BASENAME\]\]" "$DOMAIN_PATH/wiki" --include="*.md" | grep -v "$file" | wc -l)
    if [ "$REFS" -eq 0 ]; then
        echo "  孤立: $BASENAME"
    fi
done

echo ""
echo "后处理完成"
