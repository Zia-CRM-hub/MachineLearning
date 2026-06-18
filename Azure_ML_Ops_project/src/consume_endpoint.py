import argparse
from pathlib import Path

import requests
from azureml.core.webservice import Webservice

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--service-name", default="bankmarketing-service")
    parser.add_argument("--input-json", default="sample_data/sample_request.json")
    args = parser.parse_args()

    ws = get_workspace(args)
    service = Webservice(workspace=ws, name=args.service_name)

    payload = Path(args.input_json).read_text(encoding="utf-8")
    keys = service.get_keys()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys[0]}",
    }

    response = requests.post(service.scoring_uri, data=payload, headers=headers, timeout=30)
    response.raise_for_status()

    print("Status code:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    main()
