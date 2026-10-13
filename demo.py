"""
MCP-A2A Interactive Demo
=======================
Demonstrates the full lifecycle of (Agent > Tools) x (Agent > Tools).
"""

from src.orchestrator import MCPA2AOrchestrator
import json

def main():
    orchestrator = MCPA2AOrchestrator(workspace="./workspace")
    res = orchestrator.run_clean_room_pipeline(
        target_binary="/usr/bin/legacy_auth_service",
        target_symbol="_compute_request_signature"
    )
    
    print("\n📦 EVIDENCE ENVELOPE SUMMARY:")
    env = res["evidence_envelope"]
    print(f"- Producer: {env.producer_agent}")
    print(f"- Consumer: {env.consumer_agent}")
    print(f"- Evidence Records Count: {len(env.backing_tool_records)}")
    for r in env.backing_tool_records:
        print(f"  * [{r.execution_hash}] {r.tool_name}")

    print("\n🛠️ BUILD RESULT:")
    b = res["build_result"]
    print(f"- Status: {b['status']}")
    print(f"- Generated Artifact: {b['artifact_path']}")
    print(f"- Verification Suite: {b['test_result']['status']}")

if __name__ == "__main__":
    main()
