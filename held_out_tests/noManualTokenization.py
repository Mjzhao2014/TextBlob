'''
Does the solution not try to preprocess the text manually to handle tokenization?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/en/sentiments.py"

TOKENIZATION_KEYWORDS = {"split", "tokenize", "word_tokenize", "sentence_tokenize"}

def check_for_tokenization_in_class(file_path, target_class_name):
    """Check if manual tokenization functions are used in the specified class."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        tree = ast.parse(code)

        # Flag to check for tokenization functions
        tokenization_used = False

        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == target_class_name:
                # Traverse the body of the class and check for tokenization functions
                for stmt in node.body:
                    if isinstance(stmt, ast.FunctionDef):
                        for inner_stmt in ast.walk(stmt):
                            if isinstance(inner_stmt, ast.Call) and isinstance(inner_stmt.func, ast.Name):
                                if inner_stmt.func.id in TOKENIZATION_KEYWORDS:
                                    tokenization_used = True
                                    break
                if tokenization_used:
                    break

        return tokenization_used

    except FileNotFoundError:
        print(f"FAIL: File {file_path} not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"FAIL: Syntax error in file: {e}")
        sys.exit(1)

def main():
    # Specify the class name you want to check for tokenization
    target_class_name = "TransformerSentimentAnalyzer"

    # Check for tokenization-related functions in the specified class
    if check_for_tokenization_in_class(FILE_PATH, target_class_name):
        print("FAIL: Manual tokenization function used in the TransformerSentimentAnalyzer class.")
        sys.exit(1)
    else:
        print("PASS: No manual tokenization used in the TransformerSentimentAnalyzer class.")
        sys.exit(0)

if __name__ == "__main__":
    main()
