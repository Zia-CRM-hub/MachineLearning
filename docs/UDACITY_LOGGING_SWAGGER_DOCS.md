# Udacity Evidence Template: Logging, Swagger, and Documentation

Use this file while testing in the Udacity sandbox.

## 1) Enable Logging

Command used:

python src/enable_logging.py --service-name <your-service-name>

Evidence to capture:

- Screenshot of terminal output showing App Insights enabled
- Screenshot of Azure ML endpoint deployment page with diagnostics/logging visible
- Artifact file committed:
  - artifacts/service_logs.txt
  - artifacts/service_logging_status.json

Notes:

- Service name:
- Time executed:
- Result summary:

## 2) Swagger Documentation

Command used:

python src/get_swagger.py --service-name <your-service-name>

Evidence to capture:

- Screenshot of terminal output showing swagger URI
- Screenshot of swagger page or rendered schema view
- Artifact file committed:
  - artifacts/swagger.json
  - artifacts/swagger_details.json

Notes:

- Swagger URI:
- Time executed:
- Result summary:

## 3) Final Documentation Section for README

Add a short section in README that includes:

- What command enabled logging
- Proof that logging is active
- What command exported swagger
- Link to swagger URI and local artifact files
- Screenshots for both steps

Suggested bullet text:

- Logging enabled using src/enable_logging.py and validated from App Insights status in artifacts/service_logging_status.json.
- Swagger exported using src/get_swagger.py and saved at artifacts/swagger.json.

## 4) Sandbox Safety Checklist

- Commit after logging step
- Commit after swagger step
- Push immediately after each commit
- Verify screenshots are added to the repository before timeout
