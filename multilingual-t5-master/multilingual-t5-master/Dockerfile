FROM tensorflow/tensorflow:latest-gpu-jupyter

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    t5==0.9.3 \
    seqio \
    tensorflow-datasets \
    tensorflow-text \
    gin-config \
    sentencepiece \
    nltk \
    pandas \
    scikit-learn \
    jupyter \
    jupyterlab \
    ipython

# Copy project files
COPY . /workspace/

# Install the multilingual_t5 package
WORKDIR /workspace

# Expose Jupyter port
EXPOSE 8888

# Default command - start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
