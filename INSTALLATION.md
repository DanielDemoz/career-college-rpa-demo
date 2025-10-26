# 💻 Installation Guide

## Complete Setup Instructions for Career College Enrollment Automation

---

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB (8GB recommended)
- **Disk Space**: 500MB for project + 200MB for dependencies
- **Python**: 3.8 or higher (3.10+ recommended)
- **Internet**: Required for initial setup

### Recommended Specifications
- **RAM**: 8GB or more
- **CPU**: Multi-core processor (for faster processing)
- **Display**: 1920x1080 or higher (for dashboard)
- **SSD**: For faster file I/O operations

---

## 📦 Step-by-Step Installation

### Step 1: Install Python

#### Windows
1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

### Step 2: Install Tesseract OCR

Tesseract is required for document text extraction.

#### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (use default location: `C:\Program Files\Tesseract-OCR\`)
3. Add to PATH or note the installation directory
4. Verify:
   ```bash
   tesseract --version
   ```

#### macOS
```bash
brew install tesseract
```

#### Linux
```bash
sudo apt install tesseract-ocr
```

### Step 3: Download/Clone the Project

If you received this as a ZIP file:
```bash
# Extract to your desired location
cd path/to/extracted/folder
```

If cloning from Git:
```bash
git clone <repository-url>
cd Service\ two
```

### Step 4: Install Python Dependencies

Open a terminal in the project directory:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- pytesseract (OCR engine)
- Pillow (image processing)
- opencv-python (computer vision)
- pandas, numpy (data processing)
- streamlit, plotly (dashboard)
- scikit-learn (machine learning)
- And more...

**Expected installation time**: 2-5 minutes

### Step 5: Verify Installation

Run the verification script:

```bash
python run_demo.py
```

This will check if all prerequisites are met.

---

## 🎯 Quick Test

After installation, do a quick test:

```bash
# Generate sample documents
python generate_samples.py

# If successful, you should see:
# ✅ Sample documents generated successfully!
```

---

## ⚠️ Troubleshooting

### Issue 1: "Python not found" or "Command not recognized"

**Windows:**
- Python not added to PATH during installation
- Solution: Reinstall Python and check "Add Python to PATH"
- Or manually add: `C:\Python310` to PATH

**macOS/Linux:**
- Use `python3` instead of `python`
- Add alias: `alias python=python3`

### Issue 2: "Tesseract not found"

**Windows:**
```python
# Edit modules/ocr_engine.py and add at the top:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS/Linux:**
```bash
# Check if Tesseract is installed
which tesseract

# If not found, install:
# macOS: brew install tesseract
# Linux: sudo apt install tesseract-ocr
```

### Issue 3: "No module named 'module_name'"

**Solution:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Or install specific package:
pip install <module_name>
```

### Issue 4: Permission errors on Windows

**Solution:**
```bash
# Run as administrator or use:
pip install --user -r requirements.txt
```

### Issue 5: SSL/Certificate errors

**Solution:**
```bash
# Upgrade pip with trusted host
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Then install requirements
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### Issue 6: Microsoft Visual C++ errors (Windows)

Some packages require C++ build tools.

**Solution:**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Retry: `pip install -r requirements.txt`

### Issue 7: "Port 8501 already in use" (Streamlit)

**Solution:**
```bash
# Use a different port
streamlit run dashboard.py --server.port 8502
```

### Issue 8: Low OCR accuracy

**Causes:**
- Poor quality sample documents
- Tesseract not properly installed
- Missing language data

**Solution:**
```bash
# Regenerate samples
python generate_samples.py

# Install additional Tesseract language data
# Windows: During Tesseract installation, select language packs
# Linux: sudo apt install tesseract-ocr-eng
```

---

## 🔧 Advanced Configuration

### Custom Tesseract Path

Edit `modules/ocr_engine.py`:

```python
def __init__(self, tesseract_path: str = None):
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    # Or set default path here:
    else:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### Offline Installation

If you need to install on a machine without internet:

1. On a connected machine:
   ```bash
   pip download -r requirements.txt -d packages/
   ```

2. Copy the `packages/` folder to the offline machine

3. On the offline machine:
   ```bash
   pip install --no-index --find-links=packages/ -r requirements.txt
   ```

---

## 📊 Verifying Everything Works

### Test 1: Generate Samples
```bash
python generate_samples.py
```
**Expected**: Sample documents created in `sample_documents/`

### Test 2: Create Flowcharts
```bash
python create_flowcharts.py
```
**Expected**: Flowcharts created in `visualizations/`

### Test 3: Run Automation
```bash
python main.py
```
**Expected**: Processing output and reports in `output/reports/`

### Test 4: Launch Dashboard
```bash
streamlit run dashboard.py
```
**Expected**: Browser opens with interactive dashboard

### Test 5: Run Complete Demo
```bash
python run_demo.py
```
**Expected**: All steps execute successfully

---

## 🎓 For Development

### Install Additional Tools

```bash
# Code formatting
pip install black

# Linting
pip install pylint flake8

# Testing
pip install pytest pytest-cov

# Type checking
pip install mypy
```

### IDE Setup

**VS Code:**
1. Install Python extension
2. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
3. Enable format on save (Black formatter)

**PyCharm:**
1. Open project
2. Configure Python interpreter (Settings → Project → Python Interpreter)
3. Mark `modules/` as Sources Root

---

## 📱 Platform-Specific Notes

### Windows 10/11
- Use PowerShell or Command Prompt
- Antivirus may slow down OCR processing
- Windows Defender may flag first run (allow access)

### macOS
- May need to allow Python in Security & Privacy settings
- Use Terminal app
- Install Xcode Command Line Tools if prompted

### Linux (Ubuntu/Debian)
- May need to install `python3-tk` for GUI features
- Use bash or zsh terminal
- Some packages may require `build-essential`:
  ```bash
  sudo apt install build-essential python3-dev
  ```

---

## 🚀 Ready to Run!

Once installation is complete:

1. **Quick Demo**: `python run_demo.py`
2. **Manual Steps**: Follow QUICK_START.md
3. **Read Docs**: Review README.md and CASE_STUDY.md

---

## 🆘 Getting Help

### Check Documentation
- README.md - Project overview
- QUICK_START.md - Usage guide
- CASE_STUDY.md - Business context
- PROJECT_SUMMARY.md - Technical overview

### Common Issues
- Check this file's troubleshooting section
- Review error messages carefully
- Ensure all prerequisites are installed

### Still Stuck?

1. Verify Python version: `python --version` (should be 3.8+)
2. Verify Tesseract: `tesseract --version`
3. Check installed packages: `pip list`
4. Try reinstalling: `pip install -r requirements.txt --force-reinstall`

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Tesseract OCR installed
- [ ] Project files downloaded/extracted
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Sample documents generated successfully
- [ ] Flowcharts created successfully
- [ ] Main automation runs without errors
- [ ] Dashboard launches in browser

**All checked?** You're ready to go! 🎉

---

*For support, refer to the documentation files or contact the project maintainer.*

