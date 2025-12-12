---
name: schema-generator
description: Generate SQLModel/Pydantic models and SQL migration SQL from high-level schema change requests.
inputs:
- change_request: string
- existing_schema: string (optional)
outputs:
- models_code: string
- migration_sql: string
usage: Used by db-designer to output ready-to-apply model code and migration scripts.
---
