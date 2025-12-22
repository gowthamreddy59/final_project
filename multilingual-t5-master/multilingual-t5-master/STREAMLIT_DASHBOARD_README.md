# 🌍 Multilingual T5 - Streamlit Dashboard

Interactive web-based dashboard for the mT5 project setup, documentation, and configuration.

## 🚀 Quick Start

### Option 1: Simple (Windows)
**Double-click:** `run_streamlit.bat`

### Option 2: PowerShell
```powershell
.\run_streamlit.ps1
```

### Option 3: Python
```bash
python run_app.py
```

### Option 4: Direct Streamlit
```bash
streamlit run app.py
```

---

## 📖 Dashboard Pages

### 1. 🏠 **Home**
- Project overview
- Key metrics and statistics
- Quick features summary
- mT5 model sizes and capabilities

### 2. 📚 **Project Overview**
- What is mT5?
- Project structure and organization
- Core modules explanation
- File organization

### 3. 🚀 **Environment Setup**
- Three environment options compared
- Advantages and limitations of each
- Step-by-step setup instructions
- Environment comparison table

### 4. 📊 **Project Structure**
- File inventory and statistics
- Directory tree visualization
- Python files overview
- Configuration files listing

### 5. 🔧 **Configuration Guide**
- Available tasks and mixtures
- Task configuration examples
- Key parameters explanation
- Supported languages (101 languages!)

### 6. 📈 **Usage Examples**
- Basic usage patterns
- Advanced usage techniques
- Common NLP tasks (translation, QA, summarization)
- Code examples for each task

### 7. ✅ **Verification Checklist**
- Pre-setup requirements
- Installation verification
- Quick tests to run
- Environment test cases
- Resources and documentation links

---

## 🔧 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Install Streamlit
```bash
# Option 1: Using requirements file
pip install -r requirements_streamlit.txt

# Option 2: Direct installation
pip install streamlit==1.31.0 pandas numpy
```

### Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 💻 What You'll See

```
┌─────────────────────────────────────────────────┐
│  🌍 Multilingual T5 Dashboard                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Sidebar Menu:                                  │
│  • 🏠 Home                                      │
│  • 📚 Project Overview                          │
│  • 🚀 Environment Setup                         │
│  • 📊 Project Structure                         │
│  • 🔧 Configuration Guide                       │
│  • 📈 Usage Examples                            │
│  • ✅ Verification Checklist                    │
│                                                  │
│  Main Content Area:                             │
│  • Dynamic content based on selection           │
│  • Tables, code blocks, and visualizations     │
│  • Interactive elements                        │
│  • Formatted documentation                      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 📁 Files Included

```
app.py                          ← Main Streamlit application
run_app.py                      ← Python launcher script
run_streamlit.bat               ← Windows batch launcher
run_streamlit.ps1               ← PowerShell launcher
requirements_streamlit.txt      ← Python dependencies
STREAMLIT_DASHBOARD_README.md   ← This file
```

---

## 🎯 Dashboard Features

### 📊 Information Display
- **Tables:** Organized data in tabular format
- **Code Blocks:** Syntax-highlighted code examples
- **Tabs:** Organized content sections
- **Columns:** Side-by-side layout
- **Expandable Sections:** Collapsible content

### 🎨 Visual Elements
- Color-coded status indicators
- Icons for quick identification
- Professional styling
- Responsive design

### 📋 Content Sections
- Project overview and statistics
- Environment setup guides
- Code examples and usage patterns
- Configuration documentation
- Verification checklists
- Resource links

---

## 🔄 Navigation

The sidebar on the left allows you to:
1. Switch between different pages
2. View different content sections
3. Access all documentation
4. Navigate back to home

### Pages Quick Access
```
🏠 Home                          ← Start here
    ↓
📚 Project Overview              ← Understand the project
    ↓
🚀 Environment Setup             ← Choose and setup environment
    ↓
📊 Project Structure             ← Explore codebase
    ↓
🔧 Configuration Guide           ← Learn configuration
    ↓
📈 Usage Examples                ← See code examples
    ↓
✅ Verification Checklist        ← Verify your setup
```

---

## 🚀 First-Time User Guide

1. **Open the Dashboard**
   ```bash
   python run_app.py
   # or
   streamlit run app.py
   ```

2. **Start with Home Page (🏠)**
   - Get an overview of the project
   - See key statistics
   - Understand capabilities

3. **Read Project Overview (📚)**
   - Learn what mT5 is
   - Understand the structure
   - See core modules

4. **Choose Environment (🚀)**
   - Compare three options
   - Follow setup instructions
   - Pick what works for you

5. **Explore Project Structure (📊)**
   - Understand file organization
   - See available configurations
   - Review supported tasks

6. **Review Usage Examples (📈)**
   - See code patterns
   - Learn common tasks
   - Understand workflows

7. **Run Verification (✅)**
   - Check prerequisites
   - Verify installation
   - Confirm readiness

---

## 🎓 Educational Value

This dashboard serves as:
- **Documentation Portal:** Centralized access to all guides
- **Learning Tool:** Interactive exploration of the project
- **Quick Reference:** Easy lookup of information
- **Setup Assistant:** Step-by-step setup instructions
- **Code Gallery:** Examples and patterns
- **Verification Tool:** Installation checks and tests

---

## 📝 Included Documentation

The dashboard provides access to or displays:
- SETUP_GUIDE.md
- QUICK_START.md
- ENVIRONMENT_SELECTOR.txt
- DOCKER_SETUP.md
- Configuration examples
- Code samples
- Resource links

---

## 🔗 External Resources

Accessible from the dashboard:
- [Official mT5 GitHub](https://github.com/google-research/multilingual-t5)
- [Research Paper](https://arxiv.org/abs/2010.11934)
- [HuggingFace Models](https://huggingface.co/google)
- [T5 Documentation](https://github.com/google-research/text-to-text-transfer-transformer)

---

## 💡 Tips & Tricks

### Maximizing the Dashboard
- Use full-screen mode for better viewing
- Expand the sidebar for easier navigation
- Copy code examples directly to clipboard
- Bookmark important pages for quick access

### Common Tasks
- **Setup Issue?** → Go to Environment Setup page
- **Need Code Example?** → Go to Usage Examples page
- **Verify Installation?** → Go to Verification Checklist page
- **Understand Structure?** → Go to Project Structure page

---

## ⚙️ Customization

To modify the dashboard, edit `app.py`:

```python
# Change page title
st.set_page_config(
    page_title="Your Title",
    page_icon="🔧"
)

# Add new pages
page = st.sidebar.radio("Select:", [
    "🏠 Home",
    "📚 Your Page"  # Add new page
])

# Create new page logic
if page == "📚 Your Page":
    st.write("Your content here")
```

---

## 🐛 Troubleshooting

### Dashboard won't open?
```bash
# Try direct command
streamlit run app.py --logger.level=debug
```

### Port already in use?
```bash
streamlit run app.py --server.port 8502
```

### Slow performance?
- Clear Streamlit cache: `streamlit cache clear`
- Use different browser
- Check internet connection

---

## 📞 Support

### Resources
- 📖 [Streamlit Documentation](https://docs.streamlit.io/)
- 🐛 [GitHub Issues](https://github.com/google-research/multilingual-t5/issues)
- 💬 [Community Forum](https://discuss.streamlit.io/)

### Common Questions
- **Q: How do I customize the dashboard?**
  A: Edit app.py and modify the Streamlit commands

- **Q: Can I deploy this online?**
  A: Yes! Use Streamlit Cloud or AWS/GCP/Azure

- **Q: How do I add more pages?**
  A: Edit the page selection radio button and add new if/elif blocks

---

## 📄 License

Same as the mT5 project (Apache 2.0)

---

## ✨ Features Summary

✅ Interactive navigation  
✅ Professional styling  
✅ Code examples  
✅ Tables and visualizations  
✅ Comprehensive guides  
✅ Configuration reference  
✅ Verification tools  
✅ Resource links  
✅ Responsive design  
✅ Easy customization  

---

**Created:** December 2025  
**Status:** ✅ Ready to Use  
**Version:** 1.0  

Happy exploring! 🚀
