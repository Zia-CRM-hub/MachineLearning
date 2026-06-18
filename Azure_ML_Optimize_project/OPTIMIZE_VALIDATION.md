# Azure ML Optimize Project - Validation Framework

This document outlines the automated validation system for checking rubric compliance.

## Validation Notebook Structure

The `notebooks/optimize_workflow.ipynb` notebook includes comprehensive sections for validating all rubric requirements:

### Section 1: Environment Setup
- Import Azure ML SDK v1 components
- Verify Python version (3.8-3.11)
- Load workspace configuration
- Initialize artifact paths

### Section 2: Rubric Criteria Definition
- Define all 20+ rubric requirements as Python dictionary
- Structure: {category: {criterion: {required, evidence, status}}}
- Allows programmatic validation of compliance

### Section 3: Repository Artifact Discovery
- Scan project structure
- Verify presence of required files:
  - README.md with pipeline architecture
  - Source files (hyperdrive_run.py, automl_run.py, etc.)
  - Configuration templates
  - Validation notebooks

### Section 4: Documentation Validation
- Check README.md content for:
  - Pipeline architecture explanation
  - Parameter sampler benefits (grid sampling)
  - Early stopping policy benefits (Bandit policy)
  - AutoML model description (2+ sentences)
  - Model comparison (2+ sentences)
  - Improvement suggestions (2+ sentences each)

### Section 5: Code Pattern Validation
- Verify HyperDrive configuration includes:
  - GridParameterSampling with choice() expressions
  - BanditPolicy early termination
  - All hyperparameters passed as command-line arguments
  - get_best_run_by_primary_metric() method call

### Section 6: AutoML Configuration Validation
- Confirm AutoMLConfig includes all 6 required parameters:
  - task="classification"
  - primary_metric="accuracy"
  - experiment_timeout_minutes=60
  - training_data parameter
  - label_column_name="y"
  - n_cross_validations=5

### Section 7: Infrastructure Validation
- Check for ComputeTarget and AmlCompute usage
- Verify Dataset import pattern (TabularDatasetFactory or Dataset.get_by_name)
- Validate cleanup patterns

### Section 8: Artifact Inspection
- After execution, verify presence of:
  - artifacts/hyperdrive_results.json
  - artifacts/automl_results.json
  - artifacts/comparison_results.json
- Parse and validate structure of artifact files

### Section 9: Execution Metrics
- Display best run accuracy from both approaches
- Show hyperparameter values for HyperDrive best run
- Display AutoML algorithm selection
- Present side-by-side comparison

### Section 10: Compliance Scorecard
- Count passing vs. failing criteria
- Calculate rubric compliance percentage
- Generate report of missing items
- Export summary to JSON

## Validation Execution

### Pre-Execution Validation
```python
# Run notebook cells 1-7 before executing training
# These cells verify code structure without requiring Azure ML workspace
```

### During Execution
```python
# Monitor notebook cells 1-6 while HyperDrive and AutoML run
# Capture RunDetails widget screenshots
# Monitor compute cluster creation
```

### Post-Execution Validation
```python
# Run cells 8-10 after both experiments complete
# Validates all artifacts were created correctly
# Generates compliance report
```

## Expected Outputs

### Compliance Report JSON Structure
```json
{
  "timestamp": "2026-06-18T...",
  "total_criteria": 25,
  "pass_count": 23,
  "fail_count": 0,
  "unknown_count": 2,
  "compliance_percentage": 92.0,
  "missing_items": [],
  "standout_features": {
    "pipeline_diagram": "COMPLETE",
    "cloud_shell_export": "DOCUMENTED",
    "extended_automl": "DOCUMENTED", 
    "cluster_check": "COMPLETE"
  }
}
```

### Validation Outputs
1. **Artifact Manifest**: Lists all discovered files
2. **Code Pattern Analysis**: Shows detected code structures
3. **Documentation Analysis**: Text search results for required sections
4. **Compliance Checklist**: Pass/fail for each criterion
5. **Missing Items Report**: Specific action items if any

## Running the Validation

### Option 1: Complete Validation (After Execution)
```bash
# Run entire notebook to validate all requirements
# Cells 1-10, takes ~5 minutes including workspace operations
```

### Option 2: Pre-Execution Code Validation (Before Training)
```bash
# Run cells 1-7 only
# Validates code structure without executing training
# Takes ~1 minute, no Azure resource usage
```

### Option 3: Post-Execution Results Validation (After Training)
```bash
# Run cells 8-10 only
# Validates that training produced correct artifacts
# Takes ~2 minutes, minimal resource usage
```

## Validation Notebook Features

### 1. Smart Error Handling
- Try/except blocks for workspace operations
- Graceful failure if workspace unavailable
- Allows validation of code structure even without Azure access
- Clear error messages if validation steps fail

### 2. Progressive Compliance Checking
- Can run cells independently (not dependent on previous execution)
- Cell 1-3: Environment checks (can run without workspace)
- Cell 4-7: Code structure validation (no execution required)
- Cell 8-10: Results validation (requires completed runs)

### 3. Detailed Reporting
- Human-readable compliance status for each criterion
- Machine-readable JSON output for programmatic checking
- Visual comparison of HyperDrive vs. AutoML results
- Clear identification of what's ready vs. what needs work

### 4. Automatic Artifact Discovery
- Recursively scans repository structure
- Identifies all relevant files and configurations
- No manual inventory needed
- Detects new files automatically

## Validation Checkpoints

| Phase | Checkpoint | Status |
|-------|-----------|--------|
| Pre-Setup | Python 3.8-3.11 | Self-check |
| Pre-Setup | Azure ML SDK installed | Self-check |
| Pre-Execution | Repo structure correct | Cell 3 |
| Pre-Execution | Code patterns valid | Cell 5-7 |
| Post-HyperDrive | Best run retrieved | Cell 8 |
| Post-AutoML | Best model selected | Cell 8 |
| Post-Comparison | Winner determined | Cell 9 |
| Final | All artifacts present | Cell 10 |
| Final | Compliance report generated | Cell 10 |

## Tips for Best Results

1. **Run in order**: Execute notebook cells sequentially for best results
2. **Capture screenshots**: Take screenshots of RunDetails widget at cells 6 and 7
3. **Save artifacts**: Backup artifacts/ directory after each step
4. **Monitor logs**: Keep output visible for error detection
5. **Review report**: Check compliance report for any warnings

## Troubleshooting

### If workspace connection fails
- Cells 1-2 will show error but continue
- Cells 3-7 will still validate code structure
- Set `check_workspace=False` to skip workspace checks

### If artifacts are missing
- Verify HyperDrive/AutoML runs completed successfully
- Check Azure ML Studio for run details and errors
- Re-run training if necessary
- Ensure artifact paths are correct

### If validation reports failures
- Review specific criterion in RUBRIC_ASSESSMENT.md
- Check corresponding section in README.md or code files
- Make necessary updates
- Re-run validation to confirm fix

---

*Validation framework created: 2026-06-18*
