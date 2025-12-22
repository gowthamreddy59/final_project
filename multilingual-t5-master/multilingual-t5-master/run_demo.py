
import functools
import t5
import tensorflow as tf

# Check compatibility
print(f"TensorFlow version: {tf.__version__}")
try:
    import tensorflow_text
    print("TensorFlow Text imported successfully.")
except ImportError:
    print("WARNING: TensorFlow Text not found. Some features might fail.")

# Define a simple task (if possible without tf-text)
# We will just try to list available tasks or mixutres to verify T5 registry works.
print("T5 Registry:")
try:
    print(t5.data.TaskRegistry.names())
except Exception as e:
    print(f"Error accessing TaskRegistry: {e}")

# Try to load a pre-trained model path (just print it, don't download GBs yet)
print("Defining model path...")
MODEL_SIZE = "small"
PRETRAINED_DIR = f"gs://t5-data/pretrained_models/mt5/{MODEL_SIZE}"
print(f"Model directory: {PRETRAINED_DIR}")

print("Basic setup complete. Ready for iteration.")
