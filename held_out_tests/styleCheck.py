'''
Does the new code regarding the vocab file implementation follow PEP 8-compliance?
'''
import subprocess
import sys

# Files to check
FILES_TO_CHECK = [
    "/root/repo/TextBlob/src/textblob/blob.py",
    "/root/repo/TextBlob/tests/test_blob.py"
]

def check_pep8_compliance(file_path):
    """Check PEP 8 compliance using flake8."""
    try:
        # Run flake8 to check for PEP 8 compliance, including import order
        result = subprocess.run(
            ["flake8", "--max-line-length=88", "--select=E,W,F,I", file_path], capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"PASS: {file_path} is PEP 8 compliant.")
        else:
            print(f"FAIL: {file_path} is NOT PEP 8 compliant.")
            print(result.stdout)
            return False
        return True
    except FileNotFoundError:
        print(f"FAIL: File {file_path} not found.")
        return False
    except Exception as e:
        print(f"FAIL: Error running flake8 on {file_path} - {e}")
        return False

def check_pep257_compliance(file_path):
    """Check PEP 257 compliance using pydocstyle."""
    try:
        # Run pydocstyle to check for PEP 257 compliance
        result = subprocess.run(["pydocstyle", file_path], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"PASS: {file_path} is PEP 257 compliant.")
        else:
            print(f"FAIL: {file_path} is NOT PEP 257 compliant.")
            print(result.stdout)
            return False
        return True
    except FileNotFoundError:
        print(f"FAIL: File {file_path} not found.")
        return False
    except Exception as e:
        print(f"FAIL: Error running pydocstyle on {file_path} - {e}")
        return False

def main():
    # Check each file for PEP 8 and PEP 257 compliance
    for file_path in FILES_TO_CHECK:
        pep8_compliant = check_pep8_compliance(file_path)
        pep257_compliant = check_pep257_compliance(file_path)

        if not pep8_compliant or not pep257_compliant:
            sys.exit(1)  # If any check fails, exit with error status

    print("PASS: All files are PEP 8 and PEP 257 compliant.")
    sys.exit(0)

if __name__ == "__main__":
    main()
