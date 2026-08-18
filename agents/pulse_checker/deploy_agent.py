#!/usr/bin/env python3
"""
Deployment script for PulseChecker BigQuery Data Agent using geminidataanalytics.googleapis.com API.
"""

import os
import sys
import json
import requests
import subprocess

def deploy_pulse_checker_agent():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    agent_id = "pulse-checker-agent"

    print(f"Deploying PulseChecker Data Agent to Project: '{project_id}', Location: '{location}', Agent ID: '{agent_id}'...")

    # Load payload configuration
    payload_path = os.path.join(os.path.dirname(__file__), "agent_payload.json")
    with open(payload_path, "r", encoding="utf-8") as f:
        raw_payload = f.read()

    # Substitute project ID placeholder
    hydrated_payload = json.loads(raw_payload.replace("${PROJECT_ID}", project_id))

    # Obtain token via gcloud CLI
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()

    # API Endpoint
    endpoint = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/dataAgents?dataAgentId={agent_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, headers=headers, json=hydrated_payload)

    if response.status_code in [200, 201]:
        print(f"✅ Successfully created PulseChecker Data Agent! (ID: {agent_id})")
        print("Response payload:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    elif response.status_code == 409:
        print(f"Data Agent '{agent_id}' already exists. Updating agent configuration...")
        patch_endpoint = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/dataAgents/{agent_id}?updateMask=displayName,description,dataAnalyticsAgent"
        patch_response = requests.patch(patch_endpoint, headers=headers, json=hydrated_payload)
        if patch_response.status_code in [200, 201]:
            print(f"✅ Successfully updated PulseChecker Data Agent configuration! (ID: {agent_id})")
            print(json.dumps(patch_response.json(), indent=2, ensure_ascii=False))
        else:
            print("Update Status Code:", patch_response.status_code)
            print(patch_response.text)
    else:
        print(f"API Error ({response.status_code}):")
        print(response.text)

if __name__ == "__main__":
    deploy_pulse_checker_agent()
