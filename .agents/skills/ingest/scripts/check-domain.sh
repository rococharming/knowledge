#!/bin/bash
# 检查领域目录结构完整性
# 用法: ./check-domain.sh <领域路径>

DOMAIN_PATH="$1"

if [ -z "$DOMAIN_PATH" ]; then
    echo "错误: 请提供领域路径"
    echo "用法: ./check-domain.sh AI"
    exit 1
fi

ERRORS=0

# 检查必需文件
echo "=== 检查必需文件 ==="
check_path() {
    local path="$1"
    if [ ! -e "$DOMAIN_PATH/$path" ]; then
        echo "  缺失: $path"
        ERRORS=$((ERRORS + 1))
    fi
}

for file in "CLAUDE.md" "raw" "raw/articles" "raw/papers" "raw/books" "raw/videos" "raw/podcasts" "raw/others" "raw/archive" "wiki" "wiki/index.md" "wiki/log.md" "notes"; do
    check_path "$file"
done

if [ -f "$DOMAIN_PATH/CLAUDE.md" ]; then
    while IFS= read -r dir; do
        check_path "wiki/$dir"
    done < <(awk -F'`' '/^- `[^`]+\/`/ { gsub(/\/$/, "", $2); print $2 }' "$DOMAIN_PATH/CLAUDE.md")
else
    for dir in summaries entities concepts comparisons overviews syntheses recipes; do
        check_path "wiki/$dir"
    done
fi

if [ $ERRORS -eq 0 ]; then
    echo "  所有必需文件/目录都存在"
fi

# 检查 raw 下是否有未归档的素材
echo ""
echo "=== 检查未归档素材 ==="
RAW_COUNT=0
if [ -d "$DOMAIN_PATH/raw" ]; then
    RAW_COUNT=$(find "$DOMAIN_PATH/raw" -maxdepth 2 -type f ! -path "*/archive/*" ! -name ".gitkeep" | wc -l)
fi
echo "  未归档素材数: $RAW_COUNT"

# 检查 wiki 页面数
echo ""
echo "=== 检查 wiki 页面统计 ==="
if [ -f "$DOMAIN_PATH/CLAUDE.md" ]; then
    while IFS= read -r dir; do
        COUNT=0
        if [ -d "$DOMAIN_PATH/wiki/$dir" ]; then
            COUNT=$(find "$DOMAIN_PATH/wiki/$dir" -maxdepth 1 -type f -name "*.md" | wc -l)
        fi
        echo "  $dir: $COUNT"
    done < <(awk -F'`' '/^- `[^`]+\/`/ { gsub(/\/$/, "", $2); print $2 }' "$DOMAIN_PATH/CLAUDE.md")
fi

exit $ERRORS
