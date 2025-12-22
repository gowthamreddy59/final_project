
import sys
import pkg_resources

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"SUCCESS: {module_name} imported.")
        try:
            mod = __import__(module_name)
            if hasattr(mod, '__version__'):
                print(f"  Version: {mod.__version__}")
        except:
            pass
    except ImportError as e:
        print(f"FAILURE: Could not import {module_name}. Error: {e}")
    except Exception as e:
        print(f"FAILURE: Error observing {module_name}. Error: {e}")

print(f"Python version: {sys.version}")

packages = [
    'tensorflow',
    'tensorflow_text',
    't5',
    'seqio',
    'gin',
    'sentencepiece',
    'pandas'
]

print("\nChecking imports:")
for pkg in packages:
    check_import(pkg)
