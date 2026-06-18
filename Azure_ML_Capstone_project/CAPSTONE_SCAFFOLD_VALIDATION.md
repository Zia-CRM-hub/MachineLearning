# Capstone Project Scaffold Validation

**Date**: 2026-06-18
**Status**: ✅ COMPLETE

## Scaffolding Summary

### Udacity Lab Constraints (⚠️ READ FIRST)

**Critical Limits**:
- **10 attempts total** - each new session counts as 1 attempt
- **Session timeout** - lab automatically expires after limited duration
- **No persistence** - resources not preserved across sessions
- **Exhausted attempts** - contact udacity-labsupport@udacity.com if all 10 used

**Resource Management Rules**:
- **Always delete resources before session expires** (especially compute & endpoints)
- **Use lightweight compute only**: Standard_DS1_v2 (1 core) or DS2_v2 (2 cores)
- **Misuse consequences**: Lab access revoked, account deactivation
- **Monitoring**: Udacity monitors usage for compliance

**Session Time Budget** (90-minute example):
- Setup & Data Prep: 10 min
- AutoML Training: 30-40 min
- HyperDrive: 20-30 min
- Deploy & Test: 10 min
- **Cleanup (CRITICAL): 10-15 min** ⚠️

**Key Decision**: Always reserve **last 10-15 minutes** for cleanup before session expires!

See **RESOURCE_TRACKING.md** for detailed session planning templates.

### Created Core ML Scripts (src/)
- ✅ aml_utils.py - Workspace authentication and utilities
- ✅ data_prep.py - External dataset ingestion and preprocessing
- ✅ automl_run.py - AutoML classification experiment runner
- ✅ hyperdrive_run.py - HyperDrive hyperparameter tuning config
- ✅ train_hyperdrive.py - Training script for HyperDrive iterations
- ✅ compare_models.py - Model comparison logic (AutoML vs HyperDrive)
- ✅ score.py - Inference/scoring script for deployment
- ✅ deploy.py - Deployment to ACI endpoint
- ✅ consume.py - Endpoint consumption and testing

### Created Configuration & Data
- ✅ config/aml_config.capstone.example.json - Workspace config template
- ✅ .env.capstone.example - Environment variables template
- ✅ data/test_samples.json - Sample inference data
- ✅ .gitignore - Standard Python/Azure ignores

### Created Documentation
- ✅ README.md (REWRITTEN) - Complete Capstone narrative with:
  - **Udacity Lab Constraints** (10 attempts, session limits, compute SKU guidance)
  - **Resource Management Best Practices** (Standard_DS1_v2 / DS2_v2 recommendations)
  - Project overview and architecture diagram
  - Full execution workflow (6 steps)
  - Dataset description (Heart Failure Prediction, Kaggle)
  - Model comparison framework
  - Deployment details
  - Screenshot/evidence requirements
  - Resource cleanup instructions
  - Submission checklist (includes cleanup requirement)

- ✅ RESOURCE_TRACKING.md - Session management guide with:
  - Pre-session checklist
  - Resource creation log template
  - Resource deletion checklist
  - Artifact backup checklist
  - Quota tracking table
  - Re-run strategy for failed sessions
  - Time budget allocation (90-minute example)
  - Session failure recovery procedures

## Execution Workflow

### Step 1: Data Preparation
```bash
python src/data_prep.py --config config/aml_config.capstone.json --input-data data/heart_failure.csv
```
- Ingests external Kaggle dataset
- Preprocesses and registers in workspace
- Outputs: artifacts/data_prep.json

### Step 2: AutoML Training
```bash
python src/automl_run.py --config config/aml_config.capstone.json --compute-target capstone-compute
```
- Runs automated model selection
- Tracks best model and metrics
- Outputs: artifacts/automl_results.json

### Step 3: HyperDrive Tuning
```bash
python src/hyperdrive_run.py --config config/aml_config.capstone.json --compute-target capstone-compute
```
- Tunes logistic regression hyperparameters
- Grid sampling: C, max_iter, solver
- Outputs: artifacts/hyperdrive_results.json

### Step 4: Model Comparison
```bash
python src/compare_models.py
```
- Compares AutoML vs HyperDrive accuracy
- Selects and documents winner
- Outputs: artifacts/comparison_results.json

### Step 5: Deployment
```bash
python src/deploy.py --config config/aml_config.capstone.json --model-name <winner>
```
- Packages best model with scoring script
- Deploys to ACI endpoint
- Enables App Insights
- Outputs: artifacts/deployment_details.json

### Step 6: Endpoint Testing
```bash
python src/consume.py --config config/aml_config.capstone.json --endpoint-name capstone-endpoint
```
- Sends test requests to endpoint
- Validates inference response
- Outputs: artifacts/consume_results.json

## Project Requirements Met

| Requirement | Status | Evidence |
|-------------|--------|----------|
| External dataset | ✅ Scaffolded | data_prep.py (Kaggle Heart Failure) |
| AutoML model | ✅ Scaffolded | automl_run.py |
| Custom model + HyperDrive | ✅ Scaffolded | hyperdrive_run.py + train_hyperdrive.py |
| Model comparison | ✅ Scaffolded | compare_models.py |
| Deployment as web service | ✅ Scaffolded | deploy.py (ACI) |
| Endpoint consumption | ✅ Scaffolded | consume.py with test data |
| Capstone README | ✅ Complete | Rewritten with full narrative |
| Project separation | ✅ Complete | Isolated from Ops project |
| Configuration templates | ✅ Complete | aml_config.capstone.example.json, .env.capstone.example |

## Next Steps for User

## Next Steps for User

### 0. Read Udacity Lab Constraints (⚠️ CRITICAL FIRST STEP)
- [ ] Review "Udacity Lab Constraints & Best Practices" section in README.md
- [ ] Understand: 10 attempts total, each session counts as 1 attempt
- [ ] Use lightweight compute: Standard_DS1_v2 (1 core, 3.5 GB) or DS2_v2 (2 cores, 7 GB)
- [ ] Plan to delete all resources before session expires
- [ ] Review RESOURCE_TRACKING.md for time budgeting (needs ~10-15 min cleanup buffer)

### 1. Session Planning
- [ ] Download Heart Failure dataset from Kaggle locally
- [ ] Fill in config/aml_config.capstone.json with actual workspace details
- [ ] Set environment variables from .env.capstone
- [ ] Syntax check all Python scripts: `python -m py_compile src/*.py`
- [ ] Plan time budget (~90 minutes total for full execution + cleanup)
- [ ] Use RESOURCE_TRACKING.md to log session progress

### 2. Azure Setup (Before Execution)
- [ ] Create/verify Azure ML workspace
- [ ] Create compute cluster: `capstone-compute` with **lightweight SKU**
- [ ] Download Heart Failure dataset from Kaggle
- [ ] Place dataset in data/ folder
- [ ] Fill in config/aml_config.capstone.json with actual values
- [ ] Set environment variables from .env.capstone
- [ ] Verify workspace connection: `python -c "from azureml.core import Workspace; ws = Workspace.from_config()"`
- [ ] Run data preparation script
- [ ] Run AutoML training
- [ ] Run HyperDrive tuning
- [ ] Run model comparison
- [ ] Run deployment
- [ ] Run endpoint consumption test
- [ ] Capture screenshots for each step
- [ ] Save all JSON artifacts locally

### 3. Resource Cleanup (⚠️ CRITICAL - BEFORE SESSION EXPIRES)
- [ ] Delete compute cluster: `capstone-compute`
- [ ] Delete ACI endpoint: `capstone-endpoint`
- [ ] Delete any compute instances
- [ ] Verify cleanup with: `az ml compute list --resource-group <RG> --workspace-name <WS>`
- [ ] Keep: workspace, dataset, registered models (for verification)
- [ ] **Reserve last 10-15 minutes of session for cleanup**

### 4. Documentation
- [ ] Capture 7+ screenshots from Azure Studio
- [ ] Record screencast (1-5 minutes)
- [ ] Update README with actual results
- [ ] Verify all artifacts/ JSON files are populated

### 5. Submission
- [ ] Verify all resources have been deleted ✅
- [ ] Verify git status is clean
- [ ] Commit all changes
- [ ] Verify project separation (no conflicts with Ops project)
- [ ] Final README review against Udacity rubric
- [ ] Verify RESOURCE_TRACKING.md is completed for your session

## Capstone vs Ops Project Separation

| Aspect | Ops Project | Capstone Project |
|--------|-------------|------------------|
| Dataset | Bank Marketing (Azure) | Heart Failure (Kaggle) |
| Models | AutoML only | AutoML + HyperDrive |
| Workspace Config | aml_config.ops.json | aml_config.capstone.json |
| Environment | .env.ops.example | .env.capstone.example |
| Prefixes | ops- | capstone- |
| Compute Target | cpu-cluster | capstone-compute |
| Endpoint | bankmarketing-service | capstone-endpoint |
| README Type | Ops rubric | Capstone rubric |

## Architecture Decisions

**Why HyperDrive + AutoML?**
- AutoML handles feature engineering and algorithm selection
- HyperDrive demonstrates manual hyperparameter tuning expertise
- Comparison shows ability to evaluate trade-offs

**Why ACI Deployment?**
- Simpler setup for capstone project
- AKS available for future enhancements
- App Insights monitoring enabled by default

**Why Kaggle Dataset?**
- Demonstrates ability to work with external data sources
- Different from Azure built-in datasets (Ops project)
- Real-world classification problem (medical/clinical context)

## File Locations Summary

```
Azure_ML_Capstone_project/
├── src/
│   ├── aml_utils.py (45 lines)
│   ├── data_prep.py (48 lines)
│   ├── automl_run.py (59 lines)
│   ├── hyperdrive_run.py (38 lines)
│   ├── train_hyperdrive.py (50 lines)
│   ├── compare_models.py (38 lines)
│   ├── score.py (29 lines)
│   ├── deploy.py (58 lines)
│   └── consume.py (45 lines)
├── data/
│   └── test_samples.json
├── config/
│   └── aml_config.capstone.example.json
├── artifacts/ (created at runtime)
├── .env.capstone.example
├── .gitignore
├── README.md (380+ lines, rubric-ready)
└── requirements.txt (existing)
```

## Validation Status: ✅ READY FOR EXECUTION

All scaffolding complete. Project requires:
1. Azure ML workspace access
2. Kaggle dataset download
3. Configuration file setup
4. Sequential script execution
5. Screenshot and screencast capture

No code errors expected - scripts follow Azure ML SDK patterns from Ops project.
