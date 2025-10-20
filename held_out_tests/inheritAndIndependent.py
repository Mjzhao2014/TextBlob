'''
Is the new Transformer class self-contained and 
independent from other TextBlob sentiment analyzers?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "TransformerSentimentAnalyzer":
            # Ensure it inherits from BaseSentimentAnalyzer.
            if not any(isinstance(base, ast.Name) and base.id == "BaseSentimentAnalyzer" for base in node.bases):
                sys.exit(1)
            # Check if it uses PatternAnalyzer or NaiveBayesAnalyzer.
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Name) and stmt.id in {"PatternAnalyzer", "NaiveBayesAnalyzer"}:
                    sys.exit(1)
            sys.exit(0)
    sys.exit(1)
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
