'''
Does the solution import and 
use transformer.pipline() for simplicity and optimal performance?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)

    pipeline_alias = None

    # Check if pipeline is imported from transformers with or without alias
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "transformers":
            for alias in node.names:
                if alias.name == "pipeline":
                    pipeline_alias = alias.asname if alias.asname else "pipeline"

    # Check if the alias (or 'pipeline') is used as a function call
    pipeline_used = any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == pipeline_alias
        for node in ast.walk(tree)
    ) if pipeline_alias else False

    if pipeline_alias and pipeline_used:
        sys.exit(0)
    else:
        sys.exit(1)

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
