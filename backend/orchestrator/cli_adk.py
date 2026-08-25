#!/usr/bin/env python3
"""
CLI Developer Inspector for Talk to Data ADK Host Orchestrator.
Allows testing and inspecting the Orchestrator's agent routing, storytelling,
and BigQuery MCP data retrieval directly from the terminal without any UI.
"""

import os
import sys
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.host_agent import host_orchestrator

def main():
    print("=" * 80)
    print("🔍 TALK TO DATA - ADK ORCHESTRATOR TERMINAL INSPECTOR")
    print("  Interrogez directement l'Agent Hôte et observez le routage des 11 agents.")
    print("  Tapez 'exit' ou 'quit' pour quitter.")
    print("=" * 80)
    print("\n💡 Exemples de tests rapides :")
    print("  1. Présente-moi Sully")
    print("  2. Présente-moi ArenaManager")
    print("  3. Quel est l'ARPU et le chiffre d'affaires par catégorie de forfaits ?")
    print("  4. Quels sont les départements avec le plus fort stress hydrique NDVI ?\n")

    while True:
        try:
            prompt = input("\n🗣️ Vous > ").strip()
            if not prompt:
                continue
            if prompt.lower() in ["exit", "quit", "q"]:
                print("\n👋 Fermeture de l'inspecteur ADK.")
                break

            print("\n" + "-" * 50)
            print("🧠 ANALYSE ET ROUTAGE DE L'AGENT HÔTE :")
            print("-" * 50)

            # Stream response events
            stream_gen = host_orchestrator.generate_chat_stream(prompt)

            for raw_event in stream_gen:
                if not raw_event.startswith("data:"):
                    continue
                data_str = raw_event.replace("data:", "").strip()
                if not data_str:
                    continue

                try:
                    event = json.loads(data_str)
                    ev_type = event.get("type")

                    if ev_type == "thought":
                        print(f"\n💭 [PENSÉE / STORYTELLING] : {event.get('content')}")
                    elif ev_type == "switch_agent":
                        print(f"\n🔄 [BASCULE D'AGENT] : Bascule vers {event.get('agent_name')} ({event.get('agent_id')})")
                    elif ev_type == "content":
                        print(f"\n📊 [SYNTHÈSE MÉTIER] :\n{event.get('content')}")
                    elif ev_type == "error":
                        print(f"\n❌ [ERREUR] : {event.get('content')}")
                    elif ev_type == "done":
                        print("\n" + "=" * 50 + " (Fin du tour) " + "=" * 50)
                except Exception:
                    pass

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Fermeture de l'inspecteur ADK.")
            break

if __name__ == "__main__":
    main()
