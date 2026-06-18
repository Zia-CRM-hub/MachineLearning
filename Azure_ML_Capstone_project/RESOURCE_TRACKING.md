# Capstone Project - Resource Tracking & Session Management

## Purpose

Track all Azure ML resources created during Capstone execution to ensure proper cleanup before session expires.

**Critical Constraint**: 10 attempts total. Each session counts as 1 attempt. Always clean up to preserve attempts.

## Session Planning Template

### Pre-Session Checklist
- [ ] Have Kaggle Heart Failure dataset downloaded locally
- [ ] config/aml_config.capstone.json filled with workspace details
- [ ] .env.capstone environment variables set
- [ ] All 6 scripts tested for syntax (python -m py_compile src/*.py)
- [ ] Artifacts/ folder structure ready
- [ ] Decision: which compute SKU to use (Standard_DS1_v2 or DS2_v2)

### During Session - Resource Creation Log

**Session #**: _____ / 10
**Start Time**: _____ **Expected Duration**: ~60-90 minutes

#### Step 1: Data Preparation
- [ ] Dataset registered: `heart-failure-capstone`
- Output JSON: `artifacts/data_prep.json`

#### Step 2: AutoML Training
- [ ] Compute cluster created: `capstone-compute` (SKU: ____________)
- [ ] AutoML experiment: `capstone-automl`
- [ ] Model registered: `capstone-automl-model`
- Output JSON: `artifacts/automl_results.json`
- **Time elapsed**: _____ minutes

#### Step 3: HyperDrive Tuning
- [ ] Training job created via HyperDrive
- [ ] Best model identified and metrics recorded
- Output JSON: `artifacts/hyperdrive_results.json`
- **Time elapsed**: _____ minutes

#### Step 4: Model Comparison
- [ ] Winner determined (AutoML or HyperDrive)
- Output JSON: `artifacts/comparison_results.json`

#### Step 5: Deployment
- [ ] ACI endpoint created: `capstone-endpoint`
- [ ] Inference config deployed
- [ ] App Insights enabled (verify in portal)
- Output JSON: `artifacts/deployment_details.json`
- **Endpoint URI**: ________________________________________________

#### Step 6: Endpoint Testing
- [ ] Test request sent successfully
- [ ] Response validated
- Output JSON: `artifacts/consume_results.json`

### Screenshots Captured
- [ ] 1. Dataset registered page
- [ ] 2. AutoML experiment completed
- [ ] 3. HyperDrive best run
- [ ] 4. Model comparison results
- [ ] 5. Endpoint with App Insights enabled
- [ ] 6. Endpoint test successful
- [ ] 7. Swagger/API documentation

### Post-Session - Resource Deletion Log

**Session End Time**: _____ **Total Time Used**: _____ minutes

#### Resources to Delete (in order)
```
Priority 1 (Expensive/High Quota Impact):
- [ ] Compute cluster: capstone-compute
- [ ] ACI endpoint: capstone-endpoint
- [ ] Any running compute instances

Priority 2 (Storage/Optional):
- [ ] Storage account containers (if created)
- [ ] Temporary data blobs

Priority 3 (Keep for Proof):
- [ ] Dataset: heart-failure-capstone
- [ ] Registered models (all versions)
- [ ] Workspace (needed for verification)
```

#### Verification Commands
```powershell
# List all compute resources
az ml compute list --resource-group <RG> --workspace-name <WS> --query "[].name"

# List all endpoints
az ml online-endpoint list --resource-group <RG> --workspace-name <WS>

# Verify cleanup (should be empty)
az ml compute list --resource-group <RG> --workspace-name <WS> --query "length(@)"
```

#### Cleanup Status
- [ ] All compute deleted
- [ ] All endpoints deleted
- [ ] Storage verified (only datasets remain)
- [ ] Workspace accessible for verification
- **Cleanup Time**: _____ minutes
- **Date/Time Cleaned**: _____________________

## Artifact Backup Checklist

⚠️ Save these files **before** session expires:

```
artifacts/
  ├── data_prep.json (copy to local)
  ├── automl_results.json (copy to local)
  ├── hyperdrive_results.json (copy to local)
  ├── comparison_results.json (copy to local)
  ├── deployment_details.json (copy to local)
  └── consume_results.json (copy to local)

screenshots/
  ├── 01_dataset_registered.png
  ├── 02_automl_completed.png
  ├── 03_hyperdrive_best.png
  ├── 04_comparison_results.png
  ├── 05_endpoint_appinsights.png
  ├── 06_endpoint_test.png
  └── 07_swagger_ui.png
```

## Quota Tracking

### Azure ML Workspace Quotas (Typical Sandbox Limits)

| Resource | Limit | Used | Status |
|----------|-------|------|--------|
| vCPU (Standard D series) | 10 | ___ | ✅/⚠️ |
| Compute clusters | 5 | ___ | ✅/⚠️ |
| Compute instances | 3 | ___ | ✅/⚠️ |
| ACI endpoints | 10 | ___ | ✅/⚠️ |
| AKS clusters | 1 | ___ | ✅/⚠️ |

**Strategy**: Delete compute immediately after each step to stay under limits.

## Re-run Strategy (If Needed)

If you exhaust the current session and need to re-run:

1. **Minimal Re-run Path**:
   - Skip data prep (reuse registered dataset)
   - Reduce AutoML timeout from 60 to 30 minutes
   - Reduce HyperDrive iterations from 8 to 4
   - Deploy to same endpoint name (overwrite)

2. **Checkpoint System**:
   - After step 2 (AutoML): Save automl_results.json ✅
   - After step 3 (HyperDrive): Save hyperdrive_results.json ✅
   - After step 5 (Deploy): Save deployment_details.json ✅

3. **Skip Rebuilds**:
   - Can skip steps 1-4 if artifacts exist
   - Jump to step 5 with known best model
   - Only deploy and test

## Session Failure Recovery

**If session expires unexpectedly**:
1. All unsaved artifacts are lost
2. Resources may remain deployed (costing quota)
3. New session counts as next attempt
4. **Action**: Delete resources in first 5 minutes of new session before restarting

**If you hit quota limit**:
1. Cannot create new resources
2. Must delete existing resources to proceed
3. Contact udacity-labsupport@udacity.com if stuck

## Time Budget (Example: 90-minute session)

| Step | Expected Time | Cumulative | Buffer |
|------|----------------|-----------|--------|
| Setup & data prep | 10 min | 10 min | +5 min |
| AutoML training | 30-40 min | 40-50 min | +10 min |
| HyperDrive tuning | 20-30 min | 60-80 min | +5 min |
| Compare & deploy | 5 min | 65-85 min | +3 min |
| Test & screenshots | 5-10 min | 70-95 min | +5 min |
| **Cleanup** | **10 min** | **80-105 min** | ⚠️ |

**⚠️ Critical**: Reserve last 10-15 minutes for cleanup before session expires!

## Notes

- Track actual times to improve future planning
- Document any bottlenecks or unexpected issues
- Save this completed form with artifacts for reference
