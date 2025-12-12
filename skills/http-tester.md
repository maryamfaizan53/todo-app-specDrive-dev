---
name: http-tester
description: Run scripted HTTP calls (or produce curl/httpx snippets) to validate API responses and return status and JSON diff.
inputs:
- requests: list[{method, url, headers, body}]
outputs:
- responses: list[{status, body_sample, latency_ms}]
usage: Used by test-and-qa and api-designer to produce test outputs and sample validation results.
---
