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
for file in "CLAUDE.md" "raw/articles" "raw/papers" "raw/books" "raw/videos" "raw/podcasts" "raw/others" "raw/archive" "wiki/summaries" "wiki/entities" "wiki/concepts" "wiki/comparisons" "wiki/overviews" "wiki/syntheses" "wiki/recipes" "wiki/index.md" "wiki/log.md" "notes"; do
    if [ ! -e "$DOMAIN_PATH/$file" ]; then
        echo "  缺失: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

if [ $ERRORS -eq 0 ]; then
    echo "  所有必需文件/目录都存在"
fi

# 检查 raw 下是否有未归档的素材
echo ""
echo "=== 检查未归档素材 ==="
RAW_COUNT=$(find "$DOMAIN_PATH/raw" -maxdepth 2 -type f ! -path "*/archive/*" ! -name ".gitkeep" | wc -l)
echo "  未归档素材数: $RAW_COUNT"

# 检查 wiki 页面数
echo ""
echo "=== 检查 wiki 页面统计 ==="
for dir in summaries entities concepts comparisons overviews syntheses recipes; do
    COUNT=$(find "$DOMAIN_PATH/wiki/$dir" -maxdepth 1 -type f -name "*.md" | wc -l)
    echo "  $dir: $COUNT"
done

exit $ERRORS
