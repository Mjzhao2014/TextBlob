'''
Is the transformer pipeline initialized in the new transformer analyzer "__init__()" 
with “pipeline("sentiment-analysis")”?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    # Look for the import statement where pipeline is aliased
    pipeline_alias_used = False
    alias_name = None
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "transformers" and alias.asname is not None:
                    # Capture the alias used for the pipeline
                    alias_name = alias.asname
                    pipeline_alias_used = True
                    break
        if pipeline_alias_used:
            break

    # Now, check for the initialization method and ensure that the alias is used correctly
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for method in node.body:
                if isinstance(method, ast.FunctionDef) and method.name == "__init__":
                    for stmt in ast.walk(method):
                        if isinstance(stmt, ast.Call):
                            # Check if the alias is used to call pipeline
                            if isinstance(stmt.func, ast.Name) and stmt.func.id == alias_name:
                                # Ensure that the pipeline is initialized with "sentiment-analysis"
                                if any(
                                    isinstance(arg, ast.Constant) and arg.value == "sentiment-analysis"
                                    for arg in stmt.args
                                ):
                                    sys.exit(0)

    sys.exit(1)  # Fail: pipeline alias was not used correctly

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
