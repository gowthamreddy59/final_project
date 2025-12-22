
import sys
import os

# Ensure the current directory is in the path so we can import the local package
sys.path.append(os.getcwd())

print("Attempting to import multilingual_t5...")
try:
    import multilingual_t5
    print("SUCCESS: multilingual_t5 imported.")
    print(f"Package location: {multilingual_t5.__file__}")
except ImportError as e:
    print(f"FAILURE: Could not import multilingual_t5. Error: {e}")
except Exception as e:
    print(f"FAILURE: Unexpected error. Error: {e}")

print("Attempting to import multilingual_t5.tasks...")
try:
    import multilingual_t5.tasks
    print("SUCCESS: multilingual_t5.tasks imported.")
except ImportError as e:
    print(f"FAILURE: Could not import multilingual_t5.tasks. Error: {e}")
except Exception as e:
    print(f"FAILURE: Unexpected error. Error: {e}")
