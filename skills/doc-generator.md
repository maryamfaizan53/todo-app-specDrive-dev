---
name: doc-generator
description: Produce API docs, README sections, and change logs from specs and code. Produces Markdown output ready for commit.
inputs:
- spec_refs: list[string]
- code_refs: list[string]
outputs:
- docs_md: string
usage: Used by documentation subagents and plan when deliverables require human-readable docs.
---
