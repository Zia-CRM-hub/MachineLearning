import argparse
import json
from pathlib import Path

from azureml.core.webservice import Webservice

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--service-name", default="bankmarketing-service")
    args = parser.parse_args()

    ws = get_workspace(args)
    service = Webservice(workspace=ws, name=args.service_name)

    if str(service.properties.get("AppInsightsEnabled", "false")).lower() != "true":
        service.update(enable_app_insights=True)
        service.wait_for_deployment(show_output=True)

    logs = service.get_logs()
    Path("artifacts").mkdir(parents=True, exist_ok=True)
    Path("artifacts/service_logs.txt").write_text(logs, encoding="utf-8")
    Path("artifacts/service_logging_status.json").write_text(
        json.dumps(
            {
                "service_name": service.name,
                "state": service.state,
                "app_insights_enabled": service.properties.get("AppInsightsEnabled", "unknown"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Saved service logs to artifacts/service_logs.txt")
    print("Saved logging status to artifacts/service_logging_status.json")
    print("App Insights enabled:", service.properties.get("AppInsightsEnabled", "unknown"))


if __name__ == "__main__":
    main()
