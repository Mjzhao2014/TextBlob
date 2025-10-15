import ast
import sys

FILE_PATH = "/root/repo/TextBlob/tests/test_blob.py"  # Path to your test file

def check_correct_return(file_path):
    """Check that correct() returns `self.__class__(ret)` and has exactly one argument."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        # Parse the code into an AST (Abstract Syntax Tree)
        tree = ast.parse(code)

        # Find the test_correct function in the AST
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == "test_correct":
                return check_return_statement(node)
        
        # If we don't find test_correct function, report failure
        print(f"FAIL: test_correct function not found in {file_path}.")
        return False
    
    except FileNotFoundError:
        print(f"FAIL: File {file_path} not found.")
        return False
    except SyntaxError as e:
        print(f"FAIL: Syntax error in file {file_path} - {e}")
        return False


def check_return_statement(test_function_node):
    """Check that the return statement is `self.__class__(ret)` and only has one parameter."""
    for stmt in test_function_node.body:
        if isinstance(stmt, ast.Return):
            # Check if the return statement is returning `self.__class__(ret)`
            if isinstance(stmt.value, ast.Call):
                # Check if the function being called is `self.__class__`
                if isinstance(stmt.value.func, ast.Attribute) and stmt.value.func.attr == "__class__":
                    # Ensure it has exactly one argument
                    if len(stmt.value.args) == 1:
                        return True
                    else:
                        print(f"FAIL: The return statement has more than one argument.")
                        return False
            else:
                print(f"FAIL: The return statement is not `self.__class__(ret)`.")
                return False
    return False

def main():
    """Run the check for correct() return statement."""
    if not check_correct_return(FILE_PATH):
        sys.exit(1)  # If the check fails, exit with error status
    sys.exit(0)  # If the check passes, exit successfully

if __name__ == "__main__":
    main()
