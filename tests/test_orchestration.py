"""
Automated Validation Suite for MCP-A2A
"""

import unittest
import os
import shutil
from src.orchestrator import MCPA2AOrchestrator

class TestMCPA2A(unittest.TestCase):
    def setUp(self):
        self.test_workspace = "./test_workspace"
        os.makedirs(self.test_workspace, exist_ok=True)
        self.orchestrator = MCPA2AOrchestrator(workspace=self.test_workspace)

    def tearDown(self):
        if os.path.exists(self.test_workspace):
            shutil.rmtree(self.test_workspace)

    def test_pipeline_execution(self):
        result = self.orchestrator.run_clean_room_pipeline(
            target_binary="mock_binary.exe",
            target_symbol="_compute_request_signature"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["build_result"]["status"], "SUCCESS")
        self.assertEqual(result["build_result"]["test_result"]["exit_code"], 0)
        self.assertTrue(os.path.exists(result["build_result"]["artifact_path"]))

if __name__ == "__main__":
    unittest.main()
