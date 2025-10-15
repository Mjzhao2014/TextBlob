'''
Does the BaseBlob correct() function search the newly created domain vocab word set()
in order to determine whether to keep or try to correct the word?
'''

import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    vocab_searched_in_correct = False

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseBlob":
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "correct":
                    for inner_stmt in ast.walk(stmt):
                        # Look for: token.lower() in self.vocab_words
                        if isinstance(inner_stmt, ast.Compare):
                            if (
                                any(isinstance(op, ast.In) for op in inner_stmt.ops) and
                                any(
                                    isinstance(comp, ast.Attribute) and comp.attr == "vocab_words"
                                    for comp in inner_stmt.comparators
                                )
                            ):
                                vocab_searched_in_correct = True

    if vocab_searched_in_correct:
        print("PASS: BaseBlob.correct() searches self.vocab_words before correcting words.")
        sys.exit(0)
    else:
        print("FAIL: BaseBlob.correct() does NOT search self.vocab_words before correcting words.")
        sys.exit(1)

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
