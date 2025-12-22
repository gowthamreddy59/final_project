import streamlit as st
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Multilingual T5 - Setup & Demo",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .sub-header {
        font-size: 1.5em;
        color: #2ca02c;
        margin-top: 1em;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Select a page:", [
    "🏠 Home",
    "📚 Project Overview",
    "🚀 Environment Setup",
    "📊 Project Structure",
    "🔧 Configuration Guide",
    "📈 Usage Examples",
    "✅ Verification Checklist"
])

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.markdown("<h1 class='main-header'>🌍 Multilingual T5 Project</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Languages Supported", "101", "Worldwide Coverage")
    with col2:
        st.metric("🔄 Model Sizes", "5", "Small to XXL")
    with col3:
        st.metric("⚡ Setup Options", "3", "Cloud, Docker, Local")
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    **Multilingual T5 (mT5)** is a massively multilingual pre-trained text-to-text transformer model developed by Google Research.
    
    It supports 101 languages and can be used for:
    - 🌐 Machine Translation
    - ❓ Question Answering
    - 🏷️ Named Entity Recognition
    - 📝 Text Classification
    - 📄 Summarization
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-header'>🎯 Quick Features</h3>", unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        #### ☁️ Cloud Ready
        - Google Colab integration
        - Free GPU access
        - No local installation
        """)
    
    with feat_col2:
        st.markdown("""
        #### 🐳 Containerized
        - Docker support
        - Reproducible environment
        - Production-ready
        """)
    
    with feat_col3:
        st.markdown("""
        #### 💻 Flexible
        - Local Python setup
        - Full IDE integration
        - Direct control
        """)
    
    st.markdown("<h3 class='sub-header'>📊 Key Statistics</h3>", unsafe_allow_html=True)
    
    stats_data = {
        "Model": ["mT5-Small", "mT5-Base", "mT5-Large", "mT5-XL", "mT5-XXL"],
        "Parameters": ["300M", "580M", "1.2B", "3.7B", "13B"],
        "Performance": ["Good", "Better", "Very Good", "Excellent", "Outstanding"],
        "GPU Memory": ["4GB", "8GB", "12GB", "16GB", "24GB+"]
    }
    
    st.dataframe(stats_data, use_container_width=True)

# ==================== PROJECT OVERVIEW ====================
elif page == "📚 Project Overview":
    st.markdown("<h1 class='main-header'>📚 Project Overview</h1>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-header'>What is mT5?</h3>", unsafe_allow_html=True)
    st.write("""
    mT5 is a unified text-to-text transformer model that treats all NLP tasks as text generation problems.
    
    Instead of having separate models for different tasks, mT5 uses task prefixes to handle:
    - Translation
    - Question answering
    - Summarization
    - Classification
    And much more!
    """)
    
    st.markdown("<h3 class='sub-header'>📁 Project Structure</h3>", unsafe_allow_html=True)
    
    structure = """
    ```
    multilingual-t5/
    ├── multilingual_t5/
    │   ├── __init__.py
    │   ├── tasks.py                    # Task definitions
    │   ├── preprocessors.py            # Data preprocessing
    │   ├── utils.py                    # Utility functions
    │   ├── vocab.py                    # Vocabulary handling
    │   ├── preprocessors_test.py       # Tests
    │   ├── tasks_test.py               # Tests
    │   └── evaluation/
    │       ├── metrics.py              # Evaluation metrics
    │       └── metrics_test.py         # Metric tests
    ├── gin/                            # Configuration files
    │   └── sequence_lengths/
    │       ├── xnli.gin
    │       ├── pawsx.gin
    │       ├── ner.gin
    │       └── ... (other configs)
    ├── Dockerfile                      # Docker configuration
    ├── docker-compose.yml              # Docker Compose setup
    └── README.md                       # Documentation
    ```
    """
    st.code(structure, language="bash")
    
    st.markdown("<h3 class='sub-header'>🔧 Core Modules</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **tasks.py**
        - Defines all NLP tasks
        - Task mixtures
        - Training configurations
        
        **preprocessors.py**
        - Data preprocessing functions
        - Tokenization
        - Dataset preparation
        """)
    
    with col2:
        st.markdown("""
        **utils.py**
        - Utility functions
        - Helper methods
        - Common operations
        
        **evaluation/**
        - Metrics calculation
        - Performance evaluation
        - Result analysis
        """)

# ==================== ENVIRONMENT SETUP ====================
elif page == "🚀 Environment Setup":
    st.markdown("<h1 class='main-header'>🚀 Environment Setup Options</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    Choose the environment that best fits your needs. Each option has different trade-offs 
    between setup time, ease of use, and control.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["☁️ Google Colab", "🐳 Docker", "💻 Local Python"])
    
    with tab1:
        st.markdown("### ☁️ Google Colab (Recommended for Beginners)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - FREE GPU access
            - 5-minute setup
            - No installation needed
            - Cloud-based storage
            - Easy sharing
            - Pre-installed libraries
            """)
        
        with col2:
            st.markdown("""
            **⚠️ Limitations:**
            - Internet required
            - Time-limited sessions
            - Limited storage
            - Session disconnection
            - Slower than local
            """)
        
        st.markdown("---")
        st.markdown("**Quick Setup:**")
        code = """
# 1. Open Google Colab
https://colab.research.google.com/

# 2. Create new notebook or upload existing

# 3. Install dependencies
!pip install t5 seqio tensorflow-datasets

# 4. Clone repository
!git clone https://github.com/google-research/multilingual-t5.git

# 5. Run code
import multilingual_t5
# Your code here
"""
        st.code(code, language="python")
    
    with tab2:
        st.markdown("### 🐳 Docker (Production-Ready)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Reproducible environment
            - Works everywhere
            - Isolated dependencies
            - Version control
            - Team collaboration
            - Easy deployment
            """)
        
        with col2:
            st.markdown("""
            **⚠️ Limitations:**
            - Need Docker installed
            - More setup time
            - Larger disk space
            - Learning curve
            - Overhead vs local
            """)
        
        st.markdown("---")
        st.markdown("**Quick Setup:**")
        code = """
# 1. Install Docker Desktop
# https://docker.com/products/docker-desktop

# 2. Clone repository
git clone https://github.com/google-research/multilingual-t5.git
cd multilingual-t5-master

# 3. Build and run
docker-compose up -d
docker-compose exec mt5 bash

# 4. Inside container
python multilingual_t5/utils.py
"""
        st.code(code, language="bash")
    
    with tab3:
        st.markdown("### 💻 Local Python (Maximum Control)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Full local control
            - IDE integration
            - Fastest execution
            - No overhead
            - Full debugging
            - Customizable
            """)
        
        with col2:
            st.markdown("""
            **⚠️ Limitations:**
            - Complex setup (Windows)
            - Dependency conflicts
            - Longer installation
            - Version issues
            - System-dependent
            """)
        
        st.markdown("---")
        st.markdown("**Quick Setup (PowerShell):**")
        code = """
# 1. Create virtual environment
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# 2. Install dependencies
pip install tensorflow t5 seqio

# 3. Clone repository
git clone https://github.com/google-research/multilingual-t5.git

# 4. Run code
cd multilingual-t5
python multilingual_t5/utils.py
"""
        st.code(code, language="powershell")
    
    st.markdown("---")
    st.markdown("### 📊 Environment Comparison")
    
    comparison = {
        "Feature": ["Setup Time", "Learning Curve", "GPU Access", "IDE Integration", "Cost", "Best For"],
        "Colab": ["⚡ 5 min", "🟢 Easy", "✓ Free", "🔴 Limited", "$0", "Learning"],
        "Docker": ["⏱️ 15 min", "🟡 Medium", "✓ Optional", "🟢 Full", "$0-50", "Production"],
        "Local": ["⏳ 30+ min", "🔴 Hard", "✓ Own", "🟢 Full", "N/A", "Development"]
    }
    
    st.dataframe(comparison, use_container_width=True)

# ==================== PROJECT STRUCTURE ====================
elif page == "📊 Project Structure":
    st.markdown("<h1 class='main-header'>📊 Project Structure Analysis</h1>", unsafe_allow_html=True)
    
    # File statistics
    st.markdown("<h3 class='sub-header'>📁 File Inventory</h3>", unsafe_allow_html=True)
    
    files_info = {
        "Component": [
            "Core Python Files",
            "Test Files",
            "Configuration Files",
            "Documentation"
        ],
        "Count": [7, 3, 8, 2],
        "Purpose": [
            "Main functionality",
            "Unit tests",
            "Training configs",
            "Guides & README"
        ]
    }
    
    st.dataframe(files_info, use_container_width=True)
    
    # Directory structure
    st.markdown("<h3 class='sub-header'>🌳 Directory Tree</h3>", unsafe_allow_html=True)
    
    tree = """
    multilingual_t5/
    ├─ __init__.py                    [Import API modules]
    ├─ tasks.py                       [NLP task definitions]
    ├─ preprocessors.py               [Data preprocessing]
    ├─ utils.py                       [Utility functions]
    ├─ vocab.py                       [Vocabulary handling]
    ├─ *_test.py                      [Unit tests (3 files)]
    │
    ├─ evaluation/
    │  ├─ __init__.py
    │  ├─ metrics.py                  [Evaluation metrics]
    │  └─ metrics_test.py             [Metrics tests]
    │
    ├─ gin/
    │  ├─ __init__.py
    │  └─ sequence_lengths/
    │     ├─ *.gin files              [Task configs (8 files)]
    │     └─ README.md
    │
    ├─ Dockerfile                     [Docker image config]
    ├─ docker-compose.yml             [Docker orchestration]
    └─ [Documentation files]
    """
    
    st.code(tree, language="bash")
    
    # Python files overview
    st.markdown("<h3 class='sub-header'>🐍 Python Files Overview</h3>", unsafe_allow_html=True)
    
    py_files = {
        "File": ["tasks.py", "preprocessors.py", "utils.py", "vocab.py", "metrics.py"],
        "Lines (Est.)": ["~500", "~800", "~600", "~400", "~700"],
        "Purpose": [
            "Task definitions & mixtures",
            "Text preprocessing & tokenization",
            "Common utility functions",
            "Vocabulary & tokenizer",
            "Evaluation & metrics"
        ],
        "Imports": [
            "t5, seqio",
            "t5, seqio, tensorflow",
            "tensorflow, tfds",
            "seqio, sentencepiece",
            "t5, sklearn"
        ]
    }
    
    st.dataframe(py_files, use_container_width=True)
    
    # Configuration files
    st.markdown("<h3 class='sub-header'>⚙️ Configuration Files (gin/)</h3>", unsafe_allow_html=True)
    
    config_files = [
        "xnli.gin - Cross-lingual NLI task",
        "pawsx.gin - Paraphrase task",
        "tydiqa.gin - Multilingual QA",
        "xquad.gin - Cross-lingual QA",
        "ner.gin - Named entity recognition",
        "mt5_glue_v002_proportional.gin - GLUE tasks",
        "mt5_super_glue_v102_proportional.gin - SuperGLUE tasks",
        "mlqa.gin - Multilingual QA"
    ]
    
    for config in config_files:
        st.markdown(f"• `{config}`")

# ==================== CONFIGURATION GUIDE ====================
elif page == "🔧 Configuration Guide":
    st.markdown("<h1 class='main-header'>🔧 Configuration Guide</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    The mT5 project uses **Gin** configuration files to define training and evaluation tasks.
    Gin allows declarative configuration without changing code.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-header'>📋 Available Tasks</h3>", unsafe_allow_html=True)
    
    tasks = {
        "Task": [
            "XNLI",
            "PAWSX",
            "TyDiQA",
            "XQuAD",
            "WikiAnn NER",
            "GLUE",
            "SuperGLUE"
        ],
        "Type": [
            "Classification",
            "Classification",
            "QA",
            "QA",
            "NER",
            "Multi-task",
            "Multi-task"
        ],
        "Languages": [
            "15",
            "6",
            "11",
            "12",
            "40+",
            "English",
            "English"
        ],
        "Config File": [
            "xnli.gin",
            "pawsx.gin",
            "tydiqa.gin",
            "xquad.gin",
            "ner.gin",
            "mt5_glue_v002_proportional.gin",
            "mt5_super_glue_v102_proportional.gin"
        ]
    }
    
    st.dataframe(tasks, use_container_width=True)
    
    st.markdown("<h3 class='sub-header'>🎯 Task Configuration Example</h3>", unsafe_allow_html=True)
    
    st.markdown("**XNLI Task Configuration (xnli.gin):**")
    
    config_example = """
# XNLI (Cross-lingual Natural Language Inference)
# This configuration trains mT5 on the XNLI task

MIXTURE_NAME = "mt5_xnli_zeroshot"

# Model parameters
MODEL_SIZE = "large"
BATCH_SIZE = 128
LEARNING_RATE = 1e-3

# Training steps
TRAIN_STEPS = 100000
EVAL_STEPS = 5000

# Sequence lengths
SEQUENCE_LENGTH = {
    "inputs": 256,
    "targets": 256
}

# Evaluation
EVAL_FREQUENCY = 1000
KEEP_CHECKPOINT_MAX = 5
"""
    
    st.code(config_example, language="python")
    
    st.markdown("<h3 class='sub-header'>⚙️ Key Parameters</h3>", unsafe_allow_html=True)
    
    params = {
        "Parameter": [
            "MIXTURE_NAME",
            "MODEL_SIZE",
            "BATCH_SIZE",
            "LEARNING_RATE",
            "TRAIN_STEPS",
            "EVAL_STEPS",
            "SEQUENCE_LENGTH"
        ],
        "Description": [
            "Task mixture to train on",
            "Model size (small/base/large/xl/xxl)",
            "Batch size for training",
            "Learning rate",
            "Total training steps",
            "Steps between evaluations",
            "Max input/output token lengths"
        ],
        "Example": [
            "mt5_xnli_zeroshot",
            "large",
            "128",
            "1e-3",
            "100000",
            "5000",
            "{inputs: 256, targets: 256}"
        ]
    }
    
    st.dataframe(params, use_container_width=True)
    
    st.markdown("<h3 class='sub-header'>🔌 Supported Languages</h3>", unsafe_allow_html=True)
    
    languages = """
    mT5 supports **101 languages** including:
    
    African: Amharic, Hausa, Igbo, Somali, Swahili, Xhosa, Yoruba, Zulu
    
    Asian: Arabic, Bengali, Hindi, Japanese, Korean, Punjabi, Tamil, Telugu, 
            Thai, Urdu, Vietnamese, Chinese (Simplified & Traditional)
    
    European: Albanian, Bulgarian, Czech, Danish, Dutch, English, Estonian, 
              Finnish, French, German, Greek, Hungarian, Icelandic, Irish, 
              Italian, Latvian, Lithuanian, Norwegian, Polish, Portuguese, 
              Romanian, Russian, Slovak, Slovenian, Spanish, Swedish, Turkish, Ukrainian
    
    And many more...
    """
    
    st.markdown(languages)

# ==================== USAGE EXAMPLES ====================
elif page == "📈 Usage Examples":
    st.markdown("<h1 class='main-header'>📈 Usage Examples</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Basic Usage", "Advanced Usage", "Common Tasks"])
    
    with tab1:
        st.markdown("### 🎯 Basic Usage")
        
        st.markdown("**Import and Setup:**")
        code1 = """
import multilingual_t5
import t5
import tensorflow as tf

# Check available tasks
print(t5.data.TaskRegistry.names())
"""
        st.code(code1, language="python")
        
        st.markdown("**Load Pre-trained Model:**")
        code2 = """
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load mT5-Small (300M parameters)
model_name = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print(f"Model loaded: {model_name}")
print(f"Parameters: {model.num_parameters():,}")
"""
        st.code(code2, language="python")
    
    with tab2:
        st.markdown("### 🔧 Advanced Usage")
        
        st.markdown("**Working with Tasks:**")
        code3 = """
from multilingual_t5 import tasks

# Register custom task
@t5.utils.register_task("custom_translation")
def custom_translation_task(
    split,
    shuffle_buffer_size=SHUFFLE_BUFFER_SIZE,
    aims=None,
):
    '''Custom translation task'''
    ds = tf.data.Dataset.from_generator(...)
    
    return ds.map(
        functools.partial(
            t5.data.preprocessors.normalize_text,
            ...
        )
    )
"""
        st.code(code3, language="python")
        
        st.markdown("**Using Preprocessors:**")
        code4 = """
from multilingual_t5 import preprocessors

# Preprocess text
text = "Hello, how are you?"

# Tokenize
tokens = preprocessors.tokenize(text)

# Apply task prefix
prefixed = f"translate en to es: {text}"
"""
        st.code(code4, language="python")
    
    with tab3:
        st.markdown("### 📝 Common Tasks")
        
        st.markdown("**1. Translation:**")
        code_trans = """
# Example: English to Spanish
text = "Hello, how are you today?"
task_prefix = "translate en to es:"
input_text = f"{task_prefix} {text}"

input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids, max_length=50)
translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"English: {text}")
print(f"Spanish: {translation}")
"""
        st.code(code_trans, language="python")
        
        st.markdown("**2. Question Answering:**")
        code_qa = """
# Example: Open-ended QA
context = "Paris is the capital of France."
question = "What is the capital of France?"
task_prefix = "qa"
input_text = f"{task_prefix} context: {context} question: {question}"

input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids, max_length=50)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"Answer: {answer}")
"""
        st.code(code_qa, language="python")
        
        st.markdown("**3. Summarization:**")
        code_summ = """
# Example: Document summarization
document = "Paris is the capital of France. It is known for the Eiffel Tower..."
task_prefix = "summarize:"
input_text = f"{task_prefix} {document}"

input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids, max_length=50)
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"Summary: {summary}")
"""
        st.code(code_summ, language="python")

# ==================== VERIFICATION CHECKLIST ====================
elif page == "✅ Verification Checklist":
    st.markdown("<h1 class='main-header'>✅ Verification Checklist</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='success-box'>", unsafe_allow_html=True)
    st.markdown("""
    Use this checklist to verify your setup and dependencies are correctly configured.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-header'>📋 Pre-Setup Checklist</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.write("")
    with col2:
        st.checkbox("✓ Python 3.7+ installed")
        st.checkbox("✓ 8GB+ RAM available")
        st.checkbox("✓ 10GB+ free disk space")
        st.checkbox("✓ Internet connection")
        st.checkbox("✓ Git installed (for cloning)")
    
    st.markdown("<h3 class='sub-header'>🚀 Installation Verification</h3>", unsafe_allow_html=True)
    
    st.markdown("**Run this verification script:**")
    
    verify_code = """
import sys

# Check Python version
print(f"✓ Python: {sys.version}")
assert sys.version_info >= (3, 7), "Python 3.7+ required"

# Check TensorFlow
try:
    import tensorflow as tf
    print(f"✓ TensorFlow: {tf.__version__}")
except ImportError:
    print("✗ TensorFlow not installed")
    sys.exit(1)

# Check T5
try:
    import t5
    print(f"✓ T5 library available")
except ImportError:
    print("✗ T5 not installed")
    sys.exit(1)

# Check SeqIO
try:
    import seqio
    print(f"✓ SeqIO available")
except ImportError:
    print("✗ SeqIO not installed")
    sys.exit(1)

# Check multilingual_t5
try:
    import multilingual_t5
    print(f"✓ Multilingual T5 available")
except ImportError:
    print("✗ Multilingual T5 not installed")
    sys.exit(1)

# Check GPU
if tf.config.list_physical_devices('GPU'):
    print(f"✓ GPU available: {len(tf.config.list_physical_devices('GPU'))} device(s)")
else:
    print("ℹ GPU not available (CPU mode)")

print("\\n✅ All checks passed!")
"""
    
    st.code(verify_code, language="python")
    
    st.markdown("<h3 class='sub-header'>🧪 Quick Tests</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.write("")
    with col2:
        st.checkbox("✓ Import multilingual_t5 successfully")
        st.checkbox("✓ List available tasks")
        st.checkbox("✓ Load pre-trained model")
        st.checkbox("✓ Tokenize sample text")
        st.checkbox("✓ Generate predictions")
        st.checkbox("✓ Run evaluation metrics")
    
    st.markdown("<h3 class='sub-header'>🎯 Environment Tests</h3>", unsafe_allow_html=True)
    
    test_cases = {
        "Test": [
            "Import modules",
            "Load model",
            "Tokenize text",
            "Generate output",
            "Run metrics",
            "Handle languages",
            "Process batch",
            "Evaluate performance"
        ],
        "Status": [
            "✅ Pass",
            "⏳ Pending",
            "⏳ Pending",
            "⏳ Pending",
            "⏳ Pending",
            "⏳ Pending",
            "⏳ Pending",
            "⏳ Pending"
        ],
        "Time": [
            "0.1s",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-"
        ]
    }
    
    st.dataframe(test_cases, use_container_width=True)
    
    st.markdown("<h3 class='sub-header'>📚 Resources</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Documentation Links
    - 📘 [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Complete setup instructions
    - 📖 [QUICK_START.md](./QUICK_START.md) - Quick overview
    - 🐳 [DOCKER_SETUP.md](./DOCKER_SETUP.md) - Docker guide
    - 📔 [MT5_Colab_Setup.ipynb](./MT5_Colab_Setup.ipynb) - Colab notebook
    
    ### External Resources
    - 📚 [Official GitHub](https://github.com/google-research/multilingual-t5)
    - 📄 [Research Paper](https://arxiv.org/abs/2010.11934)
    - 🤗 [HuggingFace Models](https://huggingface.co/google)
    - 🔗 [T5 Documentation](https://github.com/google-research/text-to-text-transfer-transformer)
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; margin-top: 2em;">
    <p>🌍 Multilingual T5 - Streamlit Demo | Setup & Documentation Portal</p>
    <p>Created: December 2025 | <a href="https://github.com/google-research/multilingual-t5">Source</a></p>
</div>
""", unsafe_allow_html=True)
