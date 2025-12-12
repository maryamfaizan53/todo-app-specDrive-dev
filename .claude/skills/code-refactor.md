---
name: code-refactor
description: Apply safe code edits given a repo path and a patch specification. Returns a patch/diff and preview of changed lines.
inputs:
- target_paths: list[string]
- patch_instructions: string
outputs:
- diff: string
- preview: list[{path, before, after}]
usage: Used by backend-impl and frontend-impl to generate PR-ready patches.
---
