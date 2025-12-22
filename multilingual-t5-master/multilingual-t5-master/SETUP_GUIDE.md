# Multilingual T5 - Complete Setup Guide

This guide shows you three different ways to run the mT5 project in different environments.

---

## 🌐 Option 1: Google Colab (Cloud-Based) - **RECOMMENDED FOR BEGINNERS**

### ✅ Advantages:
- ✓ FREE GPU access (Tesla K80 or better)
- ✓ No installation needed
- ✓ All dependencies pre-configured
- ✓ Can run 12+ hours per session
- ✓ Excellent for learning and experimentation

### Steps:

1. **Open the Colab Notebook:**
   - Click here to open in Colab: https://colab.research.google.com/
   - Upload the `MT5_Colab_Setup.ipynb` file, or
   - Create a new notebook and copy the cells from the file

2. **Run All Cells:**
   - Runtime → Run all
   - Or run cells individually: Shift+Enter

3. **Start Using mT5:**
   - Use the examples in the notebook
   - Modify and experiment with your own code
   - Access GPU hardware for free

### Useful Colab Tips:
```python
# Mount Google Drive to save files
from google.colab import drive
drive.mount('/content/drive')

# Download files
from google.colab import files
files.download('my_file.txt')

# Upload files
uploaded = files.upload()
```

---

## 🐳 Option 2: Docker (Containerized) - **RECOMMENDED FOR PRODUCTION**

### ✅ Advantages:
- ✓ Consistent environment across machines
- ✓ Easy to share and deploy
- ✓ All dependencies isolated
- ✓ Works on Windows, Mac, and Linux
- ✓ Can use GPU with nvidia-docker

### Prerequisites:
- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- 10GB free disk space
- 8GB+ RAM

### Installation Links:
- **Windows/Mac:** https://www.docker.com/products/docker-desktop
- **Linux:** `sudo apt-get install docker.io docker-compose`

### Quick Start:

```bash
# Navigate to project directory
cd multilingual-t5-master

# Build the Docker image
docker build -t multilingual-t5:latest .

# Option A: Run with bash shell
docker run -it --rm \
  -v %cd%:/workspace \
  multilingual-t5:latest bash

# Option B: Run with Docker Compose
docker-compose up -d
docker-compose exec mt5 bash

# Option C: Run Jupyter Lab in Docker
docker-compose up
# Access at http://localhost:8888 (token: mt5password)
```

### Inside Docker Container:

```bash
# Run Python scripts
python multilingual_t5/evaluation/metrics.py

# Run tests
python -m pytest multilingual_t5/preprocessors_test.py -v

# Start Python interactive shell
python

# Install additional packages
pip install package-name
```

### GPU Support (Optional):
```bash
# Install NVIDIA Container Runtime first
# Then modify docker-compose.yml to include:
# runtime: nvidia
# environment:
#   - NVIDIA_VISIBLE_DEVICES=all
```

---

## 💻 Option 3: Local Python Virtual Environment

### ✅ Advantages:
- ✓ Direct local development
- ✓ Fastest performance
- ✓ Full control over environment
- ✓ Use your favorite IDE

### ⚠️ Challenges (Windows):
- Complex dependency resolution
- Version conflicts with TensorFlow ecosystem
- Longer setup time

### Steps (Windows PowerShell):

```powershell
# 1. Navigate to project
cd multilingual-t5-master

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies (may take 10+ minutes)
pip install tensorflow tensorflow-text tensorflow-datasets

# 5. Install core packages
pip install t5 seqio gin-config sentencepiece nltk pandas

# 6. Run the project
python multilingual_t5/utils.py
```

### Troubleshooting Common Issues:

**Problem:** `ModuleNotFoundError: No module named 'tensorflow'`
```powershell
# Solution: Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install tensorflow
```

**Problem:** `ERROR: Microsoft Visual C++ 14.0 is required`
```powershell
# Solution: Install Windows C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**Problem:** Version conflicts
```powershell
# Solution: Use specific compatible versions
pip install tensorflow==2.11.0 tensorflow-text==2.11.0
```

---

## 📊 Comparison Table

| Feature | Colab | Docker | Local venv |
|---------|-------|--------|-----------|
| **Setup Time** | <5 min | 10-20 min | 30+ min |
| **GPU Access** | ✓ Free | ✓ Paid/Own | ✓ Own only |
| **Internet Required** | Yes | Partial | No |
| **Consistency** | Perfect | Perfect | Variable |
| **Learning Curve** | Easiest | Medium | Harder |
| **For Beginners** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **For Production** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🚀 Recommended Path by Use Case

### For Learning & Experimentation:
1. **START:** Google Colab
2. **THEN:** Local virtual environment (if comfortable with Python)

### For Development:
1. **START:** Docker locally
2. **USE:** Visual Studio Code with Docker extension

### For Production Deployment:
1. **USE:** Docker with orchestration (Kubernetes)
2. **CONSIDER:** GPU cloud providers (AWS, GCP, Azure)

---

## 📚 What You Can Do with mT5

Once set up, you can:

```python
# 1. Translate between 101 languages
# 2. Summarize text in any language
# 3. Answer questions
# 4. Classify text
# 5. Extract named entities
# 6. Fine-tune on custom datasets
# 7. Export models for deployment
```

---

## 🔗 Useful Links

- **Paper:** https://arxiv.org/abs/2010.11934
- **GitHub:** https://github.com/google-research/multilingual-t5
- **HuggingFace Models:** https://huggingface.co/google
- **T5 Documentation:** https://github.com/google-research/text-to-text-transfer-transformer
- **TensorFlow Guide:** https://www.tensorflow.org/
- **Docker Tutorial:** https://docs.docker.com/

---

## ✅ Verification Checklist

After setup, verify your installation:

```python
# Run this to check everything works:

import tensorflow as tf
print(f"✓ TensorFlow: {tf.__version__}")

import t5
print(f"✓ T5 library available")

import seqio
print(f"✓ SeqIO available")

import multilingual_t5
print(f"✓ Multilingual T5 available")

print("\nYou're all set! 🎉")
```

---

## 📞 Need Help?

- **Google Colab Issues:** Check Colab documentation or AI community forums
- **Docker Issues:** See DOCKER_SETUP.md or Docker documentation
- **Dependency Issues:** Try creating a fresh virtual environment
- **mT5 Questions:** Check the official GitHub repository

Happy coding! 🚀
