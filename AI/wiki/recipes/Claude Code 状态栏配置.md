---
title: Claude Code 状态栏配置
date: 2026-05-19
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 状态栏配置

`/statusline` 用于配置 Claude Code 底部状态栏，固定显示会话状态、项目状态、Git 状态、上下文用量、token 用量等信息。

## 方式一：自动生成

直接在 Claude Code 中输入自然语言描述：

```
/statusline 显示当前模型名称、Git 分支和上下文使用百分比，并用进度条展示上下文占用情况
```

Claude Code 会根据描述生成脚本并自动更新配置。适合简单状态栏。

## 方式二：手动脚本

适合多字段、带颜色、带进度条的复杂状态栏。

### 1. 创建脚本

创建 `~/.claude/statusline.sh`：

```bash
#!/usr/bin/env bash

input="$(cat)"

# ---------- Colors ----------
RESET="\033[0m"
BOLD="\033[1m"
BLUE="\033[38;5;39m"
GREEN="\033[38;5;82m"
YELLOW="\033[38;5;220m"
ORANGE="\033[38;5;208m"
PURPLE="\033[38;5;141m"
CYAN="\033[38;5;51m"
RED="\033[38;5;203m"
GRAY="\033[38;5;245m"
LIGHT_GRAY="\033[38;5;250m"

# ---------- Basic fields ----------
MODEL="$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown-model"')"
EFFORT="$(echo "$input" | jq -r '.effort.level // "n/a"')"
THINKING_ENABLED="$(echo "$input" | jq -r '.thinking.enabled // false')"
VERSION="$(echo "$input" | jq -r '.version // "unknown"')"
DIR="$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "."')"

# ---------- Git branch ----------
if git -C "$DIR" rev-parse --git-dir >/dev/null 2>&1; then
  BRANCH="$(git -C "$DIR" branch --show-current 2>/dev/null)"
  if [ -z "$BRANCH" ]; then
    BRANCH="$(git -C "$DIR" rev-parse --short HEAD 2>/dev/null)"
  fi
else
  BRANCH="no-git"
fi

# ---------- Thinking ----------
if [ "$THINKING_ENABLED" = "true" ]; then
  THINKING="Thinking"
  THINKING_COLOR="$PURPLE"
else
  THINKING="No Thinking"
  THINKING_COLOR="$GRAY"
fi

# ---------- Context window ----------
USED_PCT_RAW="$(echo "$input" | jq -r '.context_window.used_percentage // 0')"
FREE_PCT_RAW="$(echo "$input" | jq -r '.context_window.remaining_percentage // 0')"
USED_PCT="${USED_PCT_RAW%.*}"
FREE_PCT="${FREE_PCT_RAW%.*}"
WINDOW_SIZE="$(echo "$input" | jq -r '.context_window.context_window_size // 0')"
TOTAL_IN="$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')"
TOTAL_OUT="$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')"

# ---------- Current API usage ----------
CUR_IN="$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')"
CUR_OUT="$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // 0')"
CUR_CRT="$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')"
CUR_RD="$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')"

# ---------- Format tokens ----------
fmt_tokens() {
  local n="$1"
  if [ -z "$n" ] || [ "$n" = "null" ]; then
    echo "0"
  elif [ "$n" -ge 1000000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%.1fM", n/1000000 }'
  elif [ "$n" -ge 1000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%.0fK", n/1000 }'
  else
    echo "$n"
  fi
}

# ---------- Compact progress bar ----------
BAR_WIDTH=10
FILLED=$((USED_PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
if [ "$FILLED" -gt 0 ]; then
  printf -v FILL "%${FILLED}s"
  BAR="${FILL// /█}"
fi
if [ "$EMPTY" -gt 0 ]; then
  printf -v PAD "%${EMPTY}s"
  BAR="${BAR}${PAD// /░}"
fi

# ---------- Output ----------
echo -e "${BLUE}${BOLD}${MODEL}${RESET} ${GRAY}|${RESET} ${YELLOW}${EFFORT}${RESET} ${GRAY}|${RESET} ${THINKING_COLOR}${THINKING}${RESET} ${GRAY}|${RESET} ${GREEN}v${VERSION}${RESET}"
echo -e "${CYAN}${DIR}${RESET} ${GRAY}|${RESET} ${ORANGE}${BRANCH}${RESET}"
echo -e "${PURPLE}Cxt:${RESET} ${LIGHT_GRAY}${BAR}${RESET} ${YELLOW}${USED_PCT}%${RESET}/${CYAN}${FREE_PCT}%${RESET} ${GRAY}|${RESET} ${BLUE}Size:${RESET} $(fmt_tokens "$WINDOW_SIZE") ${GRAY}|${RESET} ${GREEN}In:${RESET}$(fmt_tokens "$TOTAL_IN") ${ORANGE}Out:${RESET}$(fmt_tokens "$TOTAL_OUT")"
echo -e "${GRAY}Usage:${RESET} ${GREEN}In:${RESET}$(fmt_tokens "$CUR_IN") ${ORANGE}Out:${RESET}$(fmt_tokens "$CUR_OUT") ${YELLOW}Crt:${RESET}$(fmt_tokens "$CUR_CRT") ${CYAN}Rd:${RESET}$(fmt_tokens "$CUR_RD")"
```

创建好之后，注意给脚本赋予执行权限：

```shell
chmod +x ~/.claude/statusline.sh
```

### 2. 配置 settings.json

在 `~/settings.json` 中添加：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0,
    "refreshInterval": 5
  }
}
```

## 脚本说明

输入数据为 JSON 格式，包含以下字段：

| 字段路径 | 说明 |
|---|---|
| `.model.display_name` / `.model.id` | 模型名称 |
| `.effort.level` | 思考强度等级 |
| `.thinking.enabled` | 是否启用 thinking |
| `.version` | Claude Code 版本 |
| `.workspace.current_dir` / `.cwd` | 当前工作目录 |
| `.context_window.used_percentage` | 上下文使用百分比 |
| `.context_window.remaining_percentage` | 上下文剩余百分比 |
| `.context_window.context_window_size` | 上下文窗口总大小 |
| `.context_window.total_input_tokens` | 累计输入 token |
| `.context_window.total_output_tokens` | 累计输出 token |
| `.context_window.current_usage.*` | 当前轮次用量详情 |

## 相关页面

- [[Claude Code 内置命令]] — 所有内置命令速查

## 来源

- [[Slash Command]]
