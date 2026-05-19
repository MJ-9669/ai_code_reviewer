import ast
from typing import List, Dict, Any

class ASTAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()

        self.tree = ast.parse(self.source_code)

    def extract_structures(self) -> List[Dict[str, Any]]:
        chunks = []
        lines = self.source_code.splitlines()

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, (ast.FunctionDef. ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno
                end_line = node.end_lineno
                node_code = "\n".join(lines[start_line - 1:end_line])

                node_type = "class" if isinstance(node, ast.ClassDef) else "function"

                chunks.append({
                    "type": node_type,
                    "name": node.name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "code": node_code
                })

        return chunks
    