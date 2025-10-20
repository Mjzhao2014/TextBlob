'''
Does the solution modify the BaseBlob class correct() function 
and not the Word class correct() function?
'''
import ast
import sys

FILE_PATH = "/root/repo/TextBlob/src/textblob/blob.py"  # Path to your blob.py file

def check_word_correct_unchanged(file_path):
    """Check that the correct method in the Word class does not use self.vocab_words."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        
        # Parse the code into an AST (Abstract Syntax Tree)
        tree = ast.parse(code)
        
        word_correct_unchanged = True
        
        # Traverse the AST to find the Word class and the correct method inside it
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == "Word":
                for stmt in node.body:
                    if isinstance(stmt, ast.FunctionDef) and stmt.name == "correct":
                        # Check if `self.vocab_words` is used in the function body
                        if check_for_vocab_words_usage(stmt):
                            print("FAIL: 'self.vocab_words' found in Word.correct() method.")
                            word_correct_unchanged = False
                        
        return word_correct_unchanged

    except FileNotFoundError:
        print(f"FAIL: File {file_path} not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"FAIL: Syntax error in file: {e}")
        sys.exit(1)

def check_for_vocab_words_usage(function_node):
    """Check if `self.vocab_words` is used in the correct method."""
    for stmt in function_node.body:
        if isinstance(stmt, ast.Attribute) and stmt.attr == "vocab_words":
            return True
    return False

def main():
    """Run the check for Word.correct() to ensure it hasn't been modified with self.vocab_words."""
    if check_word_correct_unchanged(FILE_PATH):
        print("PASS: Word.correct() remains unchanged.")
        sys.exit(0)
    else:
        print("FAIL: Word.correct() was modified.")
        sys.exit(1)

if __name__ == "__main__":
    main()
