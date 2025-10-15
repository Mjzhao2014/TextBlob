'''
Does the Transformer use a pre-trained model, 
such as the default pipeline “distilbert-base-uncased-finetuned-sst-2-english” model?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "pipeline":
            if len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == "sentiment-analysis":
                sys.exit(0)
            if any(
                isinstance(arg, ast.Constant) and arg.value == "distilbert-base-uncased-finetuned-sst-2-english"
                for arg in node.args
            ):
                sys.exit(0)
    sys.exit(1)
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)