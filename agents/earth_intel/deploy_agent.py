#!/usr/bin/env python3
"""
Deployment and Update script for Earth Intel BigQuery Data Agent (earthintel-agent)
using geminidataanalytics.googleapis.com API.
"""

import os
import sys
import json
import requests
import subprocess

def deploy_earthintel_agent():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    agent_id = "earthintel-agent"

    print(f"Deploying EarthIntel Data Agent to Project: '{project_id}', Location: '{location}', Agent ID: '{agent_id}'...")

    payload_path = os.path.join(os.path.dirname(__file__), "agent_payload.json")
    with open(payload_path, "r", encoding="utf-8") as f:
        raw_payload = f.read()

    hydrated_payload = json.loads(raw_payload.replace("${PROJECT_ID}", project_id))
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Check if agent exists
    get_url = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/dataAgents/{agent_id}"
    get_resp = requests.get(get_url, headers=headers)

    if get_resp.status_code == 200:
        print(f"Data Agent '{agent_id}' already exists. Updating configuration via PATCH...")
        patch_url = f"{get_url}?updateMask=displayName,description,dataAnalyticsAgent"
        response = requests.patch(patch_url, headers=headers, json=hydrated_payload)
    else:
        print(f"Creating new Data Agent '{agent_id}' via POST...")
        post_url = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/dataAgents?dataAgentId={agent_id}"
        response = requests.post(post_url, headers=headers, json=hydrated_payload)

    if response.status_code in [200, 201]:
        print(f"✅ Successfully updated EarthIntel Data Agent configuration! (ID: {agent_id})")
        print(response.text)
    else:
        print(f"API Error ({response.status_code}):", response.text)

if __name__ == "__main__":
    deploy_earthintel_agent()
