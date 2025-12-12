---
name: web-search
description: Perform targeted web searches with domain and recency filters and return top-5 annotated results.
inputs:
- query: string
- recency_days: int (optional)
outputs:
- results: array of {title, url, date, snippet}
usage: Used by research and plan subagents to gather external references.
---
