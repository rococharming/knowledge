---
title: "Matt Pocock Skills 怎麼用在 Coding / Planning"
source: "https://university.tenten.co/t/matt-pocock-skills-coding-planning/2274"
author:
  - "[[Aiko]]"
published: 2026-06-01
created: 2026-07-15
description: "Matt Pocock Skills 怎麼用在 Coding / Planning Matt Pocock 的 mattpocock/skills 不是單一 prompt，而是一組工程型 AI Agent workflow。核心用途是：先把需求講清楚，再轉 PRD，再拆 issu"
tags:
  - "clippings"
---
#### **Matt Pocock Skills 怎麼用在 Coding / Planning**

Matt Pocock 的 `mattpocock/skills` 不是單一 prompt，而是一組工程型 AI Agent workflow。核心用途是：先把需求講清楚，再轉 PRD，再拆 issue，再用 TDD 實作，再 review / diagnose / 改架構。Repo 自述定位是「real engineering，不是 vibe coding」，並強調這些 skills 是小型、可組合、可修改的 agent skills。

## **1\. 安裝**

官方 quickstart：

```sql
npx skills@latest add mattpocock/skills
```

安裝時選你要的 coding agent，並務必選 `/setup-matt-pocock-skills`。安裝後在 agent 內先跑：

```bash
/setup-matt-pocock-skills
```

這個 setup skill 會設定 repo 的 issue tracker、triage labels、domain docs 位置，供後續 `to-prd`、`to-issues`、`tdd`、`diagnose` 等技能讀取。

## **2\. 基本觀念**

| **用途** | **Skill** | **何時用** |
| --- | --- | --- |
| 釐清需求 | `/grill-with-docs` | 開始做功能前，先讓 agent 挑戰需求、對齊 domain language、檢查現有 code 與文件 |
| 轉 PRD | `/to-prd` | 已經討論完功能，要轉成正式 PRD / GitHub issue |
| 拆工程任務 | `/to-issues` | 把 PRD 拆成可獨立實作的 vertical slices |
| 寫功能 | `/tdd` | 用 red-green-refactor 寫功能或修 bug |
| Debug | `/diagnose` | Bug、測試失敗、效能退化 |
| Review | `/review` | 對 branch / PR / WIP diff 做 spec + coding standards review |
| 看大局 | `/zoom-out` | 不懂某段 code 在整體系統的角色 |
| 改架構 | `/improve-codebase-architecture` | 找出 codebase 中 module interface 太淺、複雜度外漏、難維護的地方 |
| 交接 | `/handoff` | 長任務中斷前，產生下一個 agent 可接手的 handoff doc |

官方 reference 明確列出 engineering skills 包含 `diagnose` 、`grill-with-docs` 、`triage` 、`improve-codebase-architecture` 、`setup-matt-pocock-skills` 、`tdd` 、`to-issues` 、`to-prd` 、`zoom-out` 、`prototype` 。

## **3\. 推薦 workflow**

### **A. 新功能規劃**

```bash
/setup-matt-pocock-skills
/grill-with-docs
/to-prd
/to-issues
/tdd
/review main
```

意思：

1. 先 setup repo 規則。
2. 用 `/grill-with-docs` 把需求問清楚，並寫入 `CONTEXT.md` / ADR。
3. 用 `/to-prd` 把目前對話與 codebase 理解整理成 PRD。
4. 用 `/to-issues` 拆成 thin vertical slices。
5. 每個 issue 用 `/tdd` 實作。
6. 最後用 `/review main` 對比 main branch 檢查。

`to-issues` 的設計重點是 tracer bullet vertical slices：每個 issue 都應該是可驗證、可 demo 的端到端切片，而不是只做 schema、API、UI 其中一層。

### **B. Bug 修復**

```bash
/diagnose
/tdd
/review main
```

`diagnose` 的流程是：建立 feedback loop → reproduce → minimise → hypothesise → instrument → fix → regression-test。它強調先做可重現、可自動跑的 pass/fail signal，而不是直接猜 bug。

### **C. 架構整理**

```bash
/zoom-out
/improve-codebase-architecture
/tdd
/review main
```

適合 agent 寫太快後 codebase 變亂。官方 README 也直接指出 agent 會加速 software entropy，所以需要定期關注 system design。

## **4\. 最實用的 prompt 範本**

### **Prompt 1：第一次 setup repo**

```diff
/setup-matt-pocock-skills

This repo uses GitHub Issues.
Use these triage labels:
- needs-triage
- needs-info
- ready-for-agent
- ready-for-human
- wontfix

Use a single-context domain doc layout:
- CONTEXT.md at repo root
- ADRs in docs/adr/
```

### **Prompt 2：用 grill-with-docs 做需求釐清**

```sql
/grill-with-docs

I want to build [功能名稱].

Current goal:
[用 3-5 句描述你要做什麼]

Known constraints:
- [技術限制]
- [產品限制]
- [不能改的地方]

Please challenge the plan against the existing codebase, domain language, and ADRs.
Ask one question at a time.
For every question, provide your recommended answer.
If the answer can be found in the codebase, inspect the code instead of asking me.
```

`grill-with-docs` 會要求 agent 一次問一個問題，必要時檢查 codebase，並在術語釐清後更新 `CONTEXT.md`；當決策夠重要、難以回頭、且有 trade-off 時才建立 ADR。

### **Prompt 3：從討論內容產 PRD**

```sql
/to-prd

Create a PRD from the current conversation and codebase context.

Requirements:
- Do not add features we did not discuss.
- Use existing domain language from CONTEXT.md.
- Prefer existing test seams.
- Include user stories, implementation decisions, testing decisions, out-of-scope items.
- Publish it to the configured issue tracker.
```

`to-prd` 的原始設計是不重新訪談使用者，而是把目前 conversation context 和 codebase understanding 合成 PRD，並包含 problem、solution、user stories、implementation decisions、testing decisions、out of scope。

### **Prompt 4：把 PRD 拆成工程 tickets**

```sql
/to-issues

Break this PRD into independently implementable vertical slices.

Rules:
- Prefer many thin slices over few thick slices.
- Each slice must be demoable or verifiable on its own.
- Mark each slice as AFK or HITL.
- Show dependencies between slices.
- Use acceptance criteria.
- Do not create horizontal tasks like "build API", "build UI", "write tests" unless they are part of a complete vertical slice.
```

### **Prompt 5：用 TDD 實作單一 issue**

```diff
/tdd

Implement issue #[issue-number] using strict TDD.

Rules:
- One behavior at a time.
- Write one failing test first.
- Implement only enough code to pass that test.
- Tests must verify public behavior, not implementation details.
- Do not mock internal collaborators unless unavoidable.
- After green, refactor only when tests pass.
- Run typecheck, lint, and tests before finishing.
```

`tdd` skill 的核心原則是測 public interface 的 observable behavior，不測 implementation details；流程是 vertical red-green loop，而不是一次寫完所有 tests 再一次寫完 implementation。

### **Prompt 6：Debug**

```bash
/diagnose

Bug:
[描述錯誤]

Observed behavior:
[實際發生什麼]

Expected behavior:
[應該發生什麼]

Reproduction:
[步驟、command、URL、test、log]

Constraints:
- Do not guess before building a feedback loop.
- Create the smallest deterministic repro possible.
- Add a regression test after fixing.
```

### **Prompt 7：Review branch**

```markdown
/review main

Review this branch against main.

Check two axes:
1. Standards: does the code follow this repo's documented standards?
2. Spec: does the implementation match the originating issue / PRD?

Report:
- Blocking issues
- Non-blocking issues
- Missing tests
- Spec mismatch
- Suggested fixes
```

`review` skill 會把 diff 對固定點比較，並沿兩條軸檢查：Standards 與 Spec。它會找 issue references、PRD/spec file、repo coding standards、CONTEXT、ADR、config files 等作為 review 依據。

## **5\. 實際用法範例：做一個登入功能**

### **Step 1：先釐清**

```csharp
/grill-with-docs

I want to add email/password login to this app.

Known requirements:
- Users can sign in with email and password.
- Invalid credentials should show a safe generic error.
- Successful login redirects to dashboard.
- Existing auth/session code should be reused if available.
- Do not add OAuth in this scope.

Challenge this plan against the existing codebase.
Ask one question at a time.
Provide your recommended answer for each question.
```

### **Step 2：產 PRD**

```css
/to-prd

Create a PRD from the login discussion.
Use the existing auth terminology from CONTEXT.md.
Include out-of-scope items: OAuth, password reset, email verification.
```

### **Step 3：拆 issue**

```sql
/to-issues

Break the login PRD into vertical slices.
Each issue must include behavior, acceptance criteria, and dependency order.
Prefer AFK slices where possible.
```

可能會拆成：

| **Issue** | **類型** | **說明** |
| --- | --- | --- |
| Login form happy path | AFK | 使用者輸入正確 email/password 後登入並導向 dashboard |
| Invalid credentials handling | AFK | 錯誤帳密顯示 generic error |
| Session persistence check | AFK | 重新整理後仍維持登入狀態 |
| Auth copy / UX review | HITL | 人工確認錯誤訊息與 UX copy |

### **Step 4：實作第一個 issue**

```bash
/tdd

Implement issue #123.

Use strict red-green-refactor.
Start with the highest-level test seam available.
Do not implement invalid credential handling yet unless required by the first test.
```

### **Step 5：Review**

```csharp
/review main

Focus on:
- Does this match issue #123?
- Are tests behavior-based?
- Did we accidentally implement out-of-scope auth features?
```

## **6\. 我的使用規則**

| **情境** | **不要這樣用** | **正確用法** |
| --- | --- | --- |
| 需求還很模糊 | 直接叫 agent 開工 | 先 `/grill-with-docs` |
| 大功能 | 叫 agent 一次做完 | `/to-prd` → `/to-issues` → 每個 issue `/tdd` |
| Bug | 直接叫 agent 修 | `/diagnose` 先建立 repro loop |
| 測試 | 叫 agent 補 coverage | 用 `/tdd` 測 observable behavior |
| Review | 叫 agent “看看有沒有問題” | `/review main` ，指定 fixed point |
| 架構變亂 | 叫 agent refactor all | `/zoom-out` → `/improve-codebase-architecture` |

## **7\. 最小可行配置**

只裝這 6 個就夠：

```bash
/setup-matt-pocock-skills
/grill-with-docs
/to-prd
/to-issues
/tdd
/review
```

Debug 多的 repo 加：

```bash
/diagnose
```

大型 codebase 加：

```bash
/zoom-out
/improve-codebase-architecture
/handoff
```

## **8\. 一句話結論**

把它當成「AI 工程流程約束層」，不是 prompt library。正確順序是：

```undefined
釐清需求 → 寫 PRD → 拆 vertical issues → TDD 實作 → review → diagnose / architecture cleanup
```