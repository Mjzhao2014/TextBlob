'''
1. Does the solution use the “namedtuple” from collections to 
return the transformer sentiment analyzer result?
2. Does the new transformer sentiment analyzer class return results with an analyze() method 
to maintain consistency with the other sentiment analyzers?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)

    namedtuple_used = False
    analyze_method_exists = False

    # Traverse the AST to find the TransformerSentimentAnalyzer class
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "TransformerSentimentAnalyzer":
            for stmt in node.body:
                # Check if namedtuple() is used anywhere in the class body
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == "namedtuple":
                            namedtuple_used = True
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "analyze":
                    analyze_method_exists = True

    # If analyze method exists and namedtuple() is used anywhere in the class
    if analyze_method_exists and namedtuple_used:
        print("PASS: TransformerSentimentAnalyzer uses namedtuple() correctly.")
        sys.exit(0)
    elif not analyze_method_exists:
        print("FAIL: TransformerSentimentAnalyzer does not have an analyze() method.")
        sys.exit(1)
    else:
        print("FAIL: TransformerSentimentAnalyzer does not use namedtuple() correctly.")
        sys.exit(1)

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
