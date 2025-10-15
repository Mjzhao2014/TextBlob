'''
Does the BaseBlob __init__() have a new parameter for the custom vocab file, 
ensuring the naming is custom_vocab_file?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    vocab_param_exists = False
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseBlob":
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__":
                    for arg in stmt.args.args:
                        if arg.arg == "custom_vocab_file":
                            vocab_param_exists = True
    
    if vocab_param_exists:
        print("PASS: BaseBlob __init__() has the parameter 'custom_vocab_file'.")
        sys.exit(0)
    else:
        print("FAIL: BaseBlob __init__() does NOT have the parameter 'custom_vocab_file'.")
        sys.exit(1)
    
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)