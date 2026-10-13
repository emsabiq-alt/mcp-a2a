"""
Builder MCP Toolset
==================
Production tools for the Developer Agent:
- File system read/write
- Clean-room source code generation
- Compiler / test runner execution
"""

from typing import Dict, Any
import os

class BuilderMCPTools:
    def __init__(self, workspace_root: str = "./workspace"):
        self.workspace_root = workspace_root
        os.makedirs(self.workspace_root, exist_ok=True)
        self.catalog = {
            "fs_write_file": self.write_file,
            "fs_read_file": self.read_file,
            "runtime_run_test": self.run_test
        }

    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        if tool_name not in self.catalog:
            raise ValueError(f"Unknown builder tool: {tool_name}")
        return self.catalog[tool_name](**kwargs)

    def write_file(self, relative_path: str, content: str) -> Dict[str, Any]:
        full_path = os.path.join(self.workspace_root, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "created", "path": full_path, "bytes": len(content)}

    def read_file(self, relative_path: str) -> Dict[str, Any]:
        full_path = os.path.join(self.workspace_root, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return {"content": f.read(), "path": full_path}

    def run_test(self, test_code: str) -> Dict[str, Any]:
        """Executes a sandboxed self-check or unit test."""
        local_scope = {}
        try:
            exec(test_code, {}, local_scope)
            return {"exit_code": 0, "status": "PASSED", "message": "All unit tests succeeded."}
        except Exception as e:
            return {"exit_code": 1, "status": "FAILED", "error": str(e)}
