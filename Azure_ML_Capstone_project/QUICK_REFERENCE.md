# Capstone Quick Reference Card

⚠️ **PRINT THIS PAGE** - Keep open during session for quick reference.

---

## ⏰ SESSION TIME BUDGET (90 minutes)

```
Setup & Connect         : 10 min (00:00 - 00:10)
Data Prep              : 5 min  (00:10 - 00:15)
AutoML Training        : 35 min (00:15 - 00:50)
HyperDrive Tuning      : 20 min (00:50 - 01:10)
Compare & Deploy       : 10 min (01:10 - 01:20)
Test & Screenshots     : 5 min  (01:20 - 01:25)
Cleanup (CRITICAL!)    : 15 min (01:25 - 01:40) ⚠️
```

**KEY**: If behind schedule, skip screenshots first, but NEVER skip cleanup!

---

## 🚀 EXECUTION CHECKLIST

**Pre-Execution** ✅
- [ ] Workspace config file filled
- [ ] Environment variables set
- [ ] Python 3.11 venv created
- [ ] Kaggle dataset downloaded locally
- [ ] All scripts syntax-checked

**During Execution** (In Order)
- [ ] Step 1: `python src/data_prep.py ...` → Check artifacts/data_prep.json exists
- [ ] Step 2: `python src/automl_run.py ...` → Wait for completion → Check artifacts/automl_results.json
- [ ] Step 3: `python src/hyperdrive_run.py ...` → Check artifacts/hyperdrive_results.json
- [ ] Step 4: `python src/compare_models.py` → Check artifacts/comparison_results.json
- [ ] Step 5: `python src/deploy.py ...` → Check artifacts/deployment_details.json & endpoint URI
- [ ] Step 6: `python src/consume.py ...` → Check artifacts/consume_results.json
- [ ] Screenshots: Take at least 5 (dataset, automl, hyperdrive, deployment, test)

---

## 🛑 RESOURCE CLEANUP (Most Critical!)

**Delete BEFORE session expires (10-15 min)**:
```bash
# Delete compute cluster
az ml compute delete --name capstone-compute --resource-group <RG> --workspace-name <WS>

# Delete ACI endpoint
az ml online-endpoint delete --name capstone-endpoint --resource-group <RG> --workspace-name <WS>

# Verify cleanup (should show empty)
az ml compute list --resource-group <RG> --workspace-name <WS> --query "length(@)"
```

**Keep** (for verification):
- Workspace
- Registered dataset
- Registered models

---

## 📋 UDACITY LAB RULES

- **10 attempts total** - Use wisely!
- **Each session = 1 attempt** - Cannot be recovered
- **No persistence** - Resources deleted when session expires
- **Lightweight compute only** - DS1_v2 (1 core) or DS2_v2 (2 cores)
- **Always cleanup** - Resources cost quota
- **Session timeout** - Lab auto-expires

**If stuck**: Contact udacity-labsupport@udacity.com

---

## 💾 ARTIFACT BACKUP (Before cleanup!)

Copy to safe location:
```
artifacts/data_prep.json
artifacts/automl_results.json
artifacts/hyperdrive_results.json
artifacts/comparison_results.json
artifacts/deployment_details.json
artifacts/consume_results.json
```

---

## ⚡ QUICK COMMANDS

**Check workspace**:
```bash
az ml workspace list --query "length(@)"
```

**List resources**:
```bash
az ml compute list --resource-group <RG> --workspace-name <WS>
```

**Get endpoint URI**:
```bash
cat artifacts/deployment_details.json | grep scoring_uri
```

**Test endpoint**:
```bash
python src/consume.py --config config/aml_config.capstone.json --endpoint-name capstone-endpoint
```

---

## ⚠️ COMMON FAILURES

**Failure**: Quota exceeded
- **Fix**: Delete unused resources immediately

**Failure**: Session timeout during training
- **Fix**: Use shorter timeouts (30 min AutoML, 4 HyperDrive runs)

**Failure**: Forgot to cleanup
- **Fix**: Next session, delete in first 5 minutes before restarting

**Failure**: Can't find dataset
- **Fix**: Check `artifacts/data_prep.json` for dataset_name, verify in portal

---

## 🎯 SUCCESS CRITERIA

**Completion**:
- ✅ 6 scripts executed successfully
- ✅ All 6 JSON artifacts created
- ✅ At least 5 screenshots captured
- ✅ **All resources deleted**
- ✅ README updated with actual results
- ✅ Commit pushed to git

**Quality**:
- ✅ AutoML accuracy > 70%
- ✅ HyperDrive accuracy > 65%
- ✅ Endpoint responds with predictions
- ✅ Screencast < 5 min, clear audio

---

## 📞 SUPPORT

**Lab Issues**: udacity-labsupport@udacity.com
**Documentation**: See README.md in Azure_ML_Capstone_project/
**Tracking**: Use RESOURCE_TRACKING.md to log your session

---

**Last Updated**: 2026-06-18
**Session #**: _____ / 10
**Status**: Ready to Execute ✅
