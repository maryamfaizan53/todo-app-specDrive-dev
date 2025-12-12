---
name: db-migrator
description: Produce migration steps and example `psql`/`neon` commands to apply migrations, with safety checks and rollback suggestions.
inputs:
- migration_sql: string
- db_url: string
outputs:
- run_instructions: string
- rollback_sql: string
usage: Used by db-designer to create safe migration plans for Neon Postgres.
---
