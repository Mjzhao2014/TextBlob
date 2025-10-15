'''
Does the BaseBlob __init__() add a PEP 257-compliant comment in the class header 
that notes the new vocab file variable?
'''

import ast
import sys
import re

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    docstring_correct = False
    follows_pep257 = False
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseBlob":
            if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                docstring = node.body[0].value.s
                if re.search(r":param custom_vocab_file: .*", docstring):
                    docstring_correct = True
                
                # Ensure PEP 257 compliance (summary + proper structure)
                docstring_lines = docstring.strip().split("\n")
                if len(docstring_lines) >= 2 and docstring_lines[0].strip() and any(":param " in line for line in docstring_lines):
                    follows_pep257 = True
    
    if docstring_correct and follows_pep257:
        print("PASS: BaseBlob class docstring correctly documents 'custom_vocab_file' and follows PEP 257.")
        sys.exit(0)
    elif not docstring_correct:
        print("FAIL: BaseBlob class docstring does NOT correctly document 'custom_vocab_file'.")
        sys.exit(1)
    else:
        print("FAIL: BaseBlob class docstring does NOT follow PEP 257 formatting.")
        sys.exit(1)
    
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)