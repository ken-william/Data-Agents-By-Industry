#!/usr/bin/env python3
"""
Deploys or Updates Sully Data Agent (sully-agent) on BigQuery Conversational Analytics API (geminidataanalytics.googleapis.com).
"""

import os
import sys
import json
import subprocess
import requests

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"
AGENT_ID = "sully-agent"

BASE_URL = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents"

def get_access_token():
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
        return token
    except Exception as e:
        print(f"Error printing access token: {e}")
        sys.exit(1)

def load_payload():
    payload_path = os.path.join(os.path.dirname(__file__), "sully_payload.json")
    with open(payload_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("${PROJECT_ID}", PROJECT_ID)
    return json.loads(content)

def deploy_sully():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = load_payload()

    # 1. Check if agent exists
    agent_url = f"{BASE_URL}/{AGENT_ID}"
    resp = requests.get(agent_url, headers=headers)

    if resp.status_code == 200:
        print(f"Data Agent '{AGENT_ID}' already exists. Updating configuration...")
        update_url = f"{agent_url}?updateMask=displayName,description,dataAnalyticsAgent.publishedContext"
        resp_update = requests.patch(update_url, headers=headers, json=payload)
        if resp_update.status_code in [200, 202]:
            print(f"✅ Successfully updated Sully Data Agent configuration! (ID: {AGENT_ID})")
            print(resp_update.text)
        else:
            print(f"❌ Failed to update agent: {resp_update.status_code} - {resp_update.text}")
    else:
        print(f"Creating new Data Agent '{AGENT_ID}'...")
        create_url = f"{BASE_URL}?dataAgentId={AGENT_ID}"
        resp_create = requests.post(create_url, headers=headers, json=payload)
        if resp_create.status_code in [200, 202]:
            print(f"✅ Successfully created Sully Data Agent! (ID: {AGENT_ID})")
            print(resp_create.text)
        else:
            print(f"❌ Failed to create agent: {resp_create.status_code} - {resp_create.text}")

if __name__ == "__main__":
    print(f"Deploying Sully Data Agent to Project: '{PROJECT_ID}', Location: '{LOCATION}', Agent ID: '{AGENT_ID}'...")
    deploy_sully()
