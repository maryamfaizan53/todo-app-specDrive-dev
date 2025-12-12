---
name: repo-reader
description: Read repository files and return file summaries, code contexts, and file paths. Supports path-glob and basic token-bounded reads.
inputs:
- paths: list[string]
outputs:
- files: array of {path, content_snippet, language}
usage: Used by plan, db-designer, api-designer to inspect repo before changes.
---
