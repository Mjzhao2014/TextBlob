'''
Does the BaseBlob __init__() read in the vocab file if desired?
'''

import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    vocab_file_read = False
    vocab_file_conditionally_checked = False

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseBlob":
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__":
                    for inner_stmt in ast.walk(stmt):
                        # Detect file reading via `open(...)`
                        if isinstance(inner_stmt, ast.Call) and isinstance(inner_stmt.func, ast.Name):
                            if inner_stmt.func.id == "open":
                                vocab_file_read = True
                        # Detect conditional check of custom_vocab_file
                        if isinstance(inner_stmt, ast.If):
                            test = inner_stmt.test
                            # if custom_vocab_file:
                            if isinstance(test, ast.Name) and test.id == "custom_vocab_file":
                                vocab_file_conditionally_checked = True
                            # if custom_vocab_file is not None or similar
                            elif isinstance(test, ast.Compare):
                                if any(
                                    isinstance(comp, ast.Name) and comp.id == "custom_vocab_file"
                                    for comp in test.comparators
                                ):
                                    vocab_file_conditionally_checked = True

    if vocab_file_read and vocab_file_conditionally_checked:
        print("PASS: BaseBlob __init__() reads the vocab file (directly or via a helper function) when provided and skips when None.")
        sys.exit(0)
    elif not vocab_file_read:
        print("FAIL: BaseBlob does NOT read the vocab file (neither directly nor via a helper function).")
        sys.exit(1)
    else:
        print("FAIL: BaseBlob __init__() does NOT conditionally check for None or similar before reading the vocab file.")
        sys.exit(1)

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
