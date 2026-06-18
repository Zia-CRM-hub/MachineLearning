import argparse
import json
from pathlib import Path

import requests
from azureml.core.webservice import Webservice

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--endpoint-name", required=True)
    parser.add_argument("--test-data", required=True)
    args = parser.parse_args()

    ws = get_workspace(args.config)
    service = Webservice(workspace=ws, name=args.endpoint_name)

    # Load test data
    with open(args.test_data) as f:
        test_payload = json.load(f)

    # Get credentials
    keys = service.get_keys()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys[0]}",
    }

    # Send request
    response = requests.post(
        service.scoring_uri,
        data=json.dumps(test_payload),
        headers=headers,
        timeout=30,
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    # Save results
    with open("artifacts/consume_results.json", "w") as f:
        json.dump(
            {
                "endpoint": service.scoring_uri,
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else None,
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
