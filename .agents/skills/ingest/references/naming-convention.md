# 页面命名规范

## 命名语言

- **优先使用中文**：素材是中文的，页面标题和文件名用中文
- **英文专有名词保留原文**：如 `RAG`、`Prompt Caching`、`Claude Code`
- **混合场景**：中文描述 + 英文术语，如 `RAGvsPromptCaching`

## 文件名规则

1. **不使用路径前缀**：`wiki/summaries/文章.md` 的文件名就是 `文章.md`，不是 `summaries/文章.md`
2. **Obsidian 链接使用纯文件名**：`[[文章]]` 而非 `[[summaries/文章]]`
3. **确保文件名唯一**：不同子目录下也不应出现同名文件。如有冲突，通过调整命名区分
4. **驼峰或连字符**：推荐使用驼峰（`PromptCaching`）或保留空格（Obsidian 自动处理），避免使用下划线

## 常见命名模式

| 页面类型 | 示例 |
|---------|------|
| Summary | `ClaudeCode的PromptCaching机制深度解析.md` |
| Entity | `ClaudeCode.md`、`Anthropic.md` |
| Concept | `PromptCaching.md`、`RAG.md` |
| Comparison | `RAGvsPromptCaching.md` |
| Overview | `AI编程工具概览.md` |
| Synthesis | `LLM编程最佳实践.md` |
| Recipe | `如何配置PromptCaching.md` |
