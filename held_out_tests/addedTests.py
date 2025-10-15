'''
Does the solution add test cases to the test_blob.py file for the new custom vocab feature?
Does the solution test when at least one word is in the 
provided vocab file and should not be corrected?
'''

import ast
import sys
import subprocess

FILE_PATH = "/root/repo/TextBlob/tests/test_blob.py"

def check_for_case_insensitivity(test_function_code):
    """Check if the code contains both 'Xray' and 'xray' for case insensitivity."""
    if 'Xray' in test_function_code and 'xray' in test_function_code:
        return True
    return False

try:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)

    custom_vocab_tests_added = False
    has_test_correct_function = False
    test_for_case_insensitivity = False

    # Search for the `test_correct` function in the `TestTextBlob` class
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "TextBlobTest":
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "test_correct_custom_vocab":
                    has_test_correct_function = True
                    # Check if custom vocab file is being used in the test
                    if "custom_vocab_file" in ast.get_source_segment(code, stmt):
                        custom_vocab_tests_added = True
                    # Check for case insensitivity test (presence of both "xray" and "Xray")
                    if check_for_case_insensitivity(ast.get_source_segment(code, stmt)):
                        test_for_case_insensitivity = True

    # Final checks: if custom vocab tests and case insensitivity test are found
    if custom_vocab_tests_added and has_test_correct_function and test_for_case_insensitivity:
        # Run pytest to ensure tests pass
        test_command = f"pytest -q {FILE_PATH} --tb=short --disable-warnings"
        result = subprocess.run(test_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("PASS: TestTextBlob includes custom vocab file tests in test_correct(), and all tests pass.")
            sys.exit(0)
        else:
            print("FAIL: TestTextBlob includes custom vocab tests in test_correct(), but some tests failed.")
            print(result.stdout)
            sys.exit(1)
    elif not has_test_correct_function:
        print("FAIL: No test_correct function found in TextBlobTest in test_blob.py.")
        sys.exit(1)
    elif not custom_vocab_tests_added:
        print("FAIL: No custom vocab tests found in test_correct() in TextBlobTest in test_blob.py.")
        sys.exit(1)
    elif not test_for_case_insensitivity:
        print("FAIL: No case-insensitive custom vocab matching tests (e.g., 'xray' and 'Xray') found.")
        sys.exit(1)

except FileNotFoundError:
    print(f"FAIL: File {FILE_PATH} not found.")
    sys.exit(1)
except SyntaxError as e:
    print(f"FAIL: Syntax error in file: {e}")
    sys.exit(1)
