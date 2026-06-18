# Project Separation Validation

Validated projects:
- Azure_ML_Ops_project
- Azure_ML_Capstone_project

## Isolation Checklist

1. Separate folders
- Ops: `Azure_ML_Ops_project/`
- Capstone: `Azure_ML_Capstone_project/`

2. Separate dependency files
- Ops: `Azure_ML_Ops_project/requirements.txt`
- Capstone: `Azure_ML_Capstone_project/requirements.txt`

3. Separate workspace config templates
- Ops: `Azure_ML_Ops_project/config/aml_config.ops.example.json`
- Capstone: `Azure_ML_Capstone_project/config/aml_config.capstone.example.json`

4. Separate environment variable templates
- Ops: `Azure_ML_Ops_project/.env.ops.example`
- Capstone: `Azure_ML_Capstone_project/.env.capstone.example`

5. Separate virtual environments (recommended)
- Ops: `Azure_ML_Ops_project/.venv`
- Capstone: `Azure_ML_Capstone_project/.venv`

## Notes

- Do not reuse endpoint names and pipeline names across projects.
- Use project-specific prefixes (`ops-`, `capstone-`) to avoid Azure resource collisions.
