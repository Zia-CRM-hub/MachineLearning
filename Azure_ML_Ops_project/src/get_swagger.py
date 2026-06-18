import argparse
import json
import os

from azureml.core.webservice import Webservice

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--service-name", default="bankmarketing-service")
    args = parser.parse_args()

    ws = get_workspace(args)
    service = Webservice(workspace=ws, name=args.service_name)

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/swagger.json", "w", encoding="utf-8") as f:
        json.dump(service.swagger, f, indent=2)
    with open("artifacts/swagger_details.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "service_name": service.name,
                "state": service.state,
                "swagger_uri": service.swagger_uri,
                "scoring_uri": service.scoring_uri,
            },
            f,
            indent=2,
        )

    print("Swagger URI:", service.swagger_uri)
    print("Saved swagger spec to artifacts/swagger.json")
    print("Saved swagger metadata to artifacts/swagger_details.json")


if __name__ == "__main__":
    main()
