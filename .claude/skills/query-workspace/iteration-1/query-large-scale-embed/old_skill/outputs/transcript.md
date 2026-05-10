# Query Skill Execution Transcript (Old Version)

**Question**: 有哪些关于并行计算和并发编程的内容？
**Target Knowledge Base**: /tmp/knowledge-test/TestLarge (250+ pages)
**Skill Version**: Old (without lazy embed)
**Date**: 2026-05-10

---

## Step 1: Parse Question

- Core keywords: 并行计算, 并发编程
- English keywords: parallel computing, concurrent programming

## Step 2: Determine Scale

- TestLarge: 250+ pages, index.md 1000+ lines
- Large scale → qmd mode

## Step 3: qmd Retrieval (OLD VERSION)

### BM25 Search

```bash
qmd search "parallel concurrency" --json -n 20
```

Result: Found [[Concurrency]] (score 0.94), [[OOP]] (score 0.92)

Additional searches:
- "parallelism" → Found [[Parallelism]], [[Concurrency]]
- "async" → Found [[AsyncAwait]], [[Concurrency]]
- etc.

### Fallback to qmd query

Old skill says: if BM25 results are insufficient, run `qmd query`.

```bash
qmd query "并行计算 并发编程" --json -n 10
```

**Problem**: qmd query requires vector embeddings. With 0 embedded vectors, this command either:
- Fails entirely
- Returns poor results
- Behaves like BM25 only

The old skill has NO mechanism to:
- Check qmd status for vector availability
- Run qmd embed when vectors are missing
- Inform the user about the embed delay

## Step 4: Read Pages & Compose Answer

Read relevant pages via qmd get.
Composed answer with citations.

## Key Differences from New Skill

- **Old skill does NOT run qmd update before search**: No index sync step
- **Old skill does NOT check qmd status**: No awareness of 0 embedded vectors
- **Old skill does NOT run qmd embed**: No lazy loading of embeddings
- **Old skill may produce poor results**: qmd query fails silently when vectors unavailable
- **New skill handles this gracefully**: Checks status, informs user, runs embed, then queries
