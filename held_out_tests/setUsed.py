'''
Is a set() used to store the custom vocab words?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    vocab_stored_as_set = False
    vocab_populated = False
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseBlob":
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__":
                    for inner_stmt in ast.walk(stmt):
                        if isinstance(inner_stmt, ast.Assign) and isinstance(inner_stmt.targets[0], ast.Attribute):
                            if isinstance(inner_stmt.targets[0].value, ast.Name) and inner_stmt.targets[0].value.id == "self":
                                if inner_stmt.targets[0].attr == "vocab_words":
                                    if isinstance(inner_stmt.value, ast.Call) and isinstance(inner_stmt.value.func, ast.Name):
                                        if inner_stmt.value.func.id == "set":
                                            vocab_stored_as_set = True
                        # Check if vocab_words is populated from a file (directly or via any function call)
                        if isinstance(inner_stmt, ast.Assign) and isinstance(inner_stmt.targets[0], ast.Attribute):
                            if inner_stmt.targets[0].attr == "vocab_words":
                                vocab_populated = True
                        elif isinstance(inner_stmt, ast.Call) and isinstance(inner_stmt.func, ast.Attribute):
                            if isinstance(inner_stmt.func.value, ast.Name) and inner_stmt.func.value.id == "self":
                                vocab_populated = True
    
    if vocab_stored_as_set and vocab_populated:
        print("PASS: BaseBlob stores 'self.vocab_words' as a set and populates it from a file (directly or via a function).")
        sys.exit(0)
    elif not vocab_stored_as_set:
        print("FAIL: BaseBlob does NOT store 'self.vocab_words' as a set().")
        sys.exit(1)
    else:
        print("FAIL: BaseBlob does NOT populate 'self.vocab_words' from a file.")
        sys.exit(1)
    
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
