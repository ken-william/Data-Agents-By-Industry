#!/usr/bin/env python3
"""
Deploy / Update all 11 Data Agents on GCP Vertex AI Data Agents.
"""

import os
import sys
import subprocess
import time

AGENTS = [
    "cine_analyst",
    "net_arch",
    "credit_advisor",
    "earth_intel",
    "transit_navigator",
    "sully",
    "pulse_checker",
    "shelf_optimizer",
    "arena_manager",
    "helios",
    "ceres"
]

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
TALKTODATA_DIR = os.path.dirname(os.path.abspath(__file__))

def deploy_agent(agent_name):
    script_path = os.path.join(TALKTODATA_DIR, "agents", agent_name, "deploy_agent.py")
    if not os.path.exists(script_path):
        print(f"⚠️ Script not found for '{agent_name}': {script_path}")
        return False

    print(f"\n🚀 Deploying '{agent_name}'...")
    env = os.environ.copy()
    env["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

    for attempt in range(1, 4):
        res = subprocess.run([sys.executable, script_path], env=env, capture_output=True, text=True)
        if res.returncode == 0 and "Successfully updated" in res.stdout:
            print(f"  ✅ Successfully deployed '{agent_name}'!")
            return True
        else:
            print(f"  ⚠️ Attempt {attempt} failed for '{agent_name}'. Output:\n{res.stdout}\n{res.stderr}")
            time.sleep(3)
    return False

def main():
    print(f"Deploying all 11 Data Agents to Project '{PROJECT_ID}'...")
    success_count = 0
    for agent in AGENTS:
        if deploy_agent(agent):
            success_count += 1
        time.sleep(1)

    print(f"\n=========================================")
    print(f"DEPLOYMENT SUMMARY: {success_count}/{len(AGENTS)} agents successfully deployed!")
    print(f"=========================================")

if __name__ == "__main__":
    main()
