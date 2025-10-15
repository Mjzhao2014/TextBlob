'''
Can the transformer class model used be easily changed, 
without modifying the class, via an argument?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    model_param_exists = False
    model_set_as_class_variable = False
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "TransformerSentimentAnalyzer":
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__":
                    for arg in stmt.args.args:
                        if arg.arg == "model_name":
                            model_param_exists = True
                    for inner_stmt in ast.walk(stmt):
                        if isinstance(inner_stmt, ast.Assign):
                            for target in inner_stmt.targets:
                                if isinstance(target, ast.Attribute) and target.attr == "model_name":
                                    model_set_as_class_variable = True
    
    if model_param_exists and model_set_as_class_variable:
        print("PASS: TransformerSentimentAnalyzer allows flexible model configuration via 'model_name' parameter.")
        sys.exit(0)
    elif not model_param_exists:
        print("FAIL: TransformerSentimentAnalyzer __init__ does not have 'model_name' as a parameter.")
        sys.exit(1)
    else:
        print("FAIL: 'model_name' parameter is not assigned as a class variable in TransformerSentimentAnalyzer.")
        sys.exit(1)
    
except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
