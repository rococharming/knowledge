---
name: defuddle
description: 使用 Defuddle CLI 从网页中提取干净的 Markdown 内容，移除导航和杂乱信息以节省 token。当用户提供一个要读取或分析的 URL 时，或针对在线文档、文章、博客文章或任何标准网页，请使用此工具代替 WebFetch。对于以 .md 结尾的 URL 请勿使用 —— 它们已经是 Markdown，直接使用 WebFetch 即可。
---

# Defuddle

使用 Defuddle CLI 从网页中提取干净的可读内容。对于标准网页，优先于 WebFetch 使用 —— 它能移除导航栏、广告和杂乱内容，减少 token 使用量。

如果未安装，请执行：`npm install -g defuddle`

## 用法

始终使用 `--md` 参数输出 Markdown：

```bash
defuddle parse <url> --md
```

保存到文件：

```bash
defuddle parse <url> --md -o content.md
```

提取特定元数据：

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## 输出格式

| 参数 | 格式 |
|------|--------|
| `--md` | Markdown（默认选择） |
| `--json` | JSON，包含 HTML 和 Markdown |
| （无） | HTML |
| `-p <name>` | 特定元数据属性 |
