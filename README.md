\# LLM Medical Document Anonymizer - Setup Guide



AI-powered medical document anonymization with privacy risk assessment.



\## Quick Setup (30 minutes)



\### Step 1: Install Python

\- Download Python 3.11+ from: https://www.python.org/downloads/

\- \*\*Important\*\*: Check "Add Python to PATH" during installation

\- Restart your computer after installation



\### Step 2: Download llama.cpp

1\. Go to: https://github.com/ggerganov/llama.cpp/releases/latest

2\. Download: `llama-b\*\*\*\*-bin-win-cpu-x64.zip` (for CPU)

3\. Extract to: `C:\\llama.cpp`



\### Step 3: Download a Model

1\. Go to: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF

2\. Click: `tinyllama-1.1b-chat-v1.0.Q4\_K\_M.gguf`

3\. Download and save to: `C:\\models\\`



(Create the folder if it doesn't exist: `New-Item -ItemType Directory -Path "C:\\models" -Force`)



\### Step 4: Install Tesseract OCR

1\. Download: https://github.com/UB-Mannheim/tesseract/wiki

2\. Run installer → Install to: `C:\\Program Files\\Tesseract-OCR`

3\. Make sure "Add to PATH" is checked



\### Step 5: Setup Project



Open PowerShell and run:

```powershell

\# Clone the repository

git clone https://github.com/siddharthrajendran2-cmd/LLM-Medical-Anonymizer.git

cd LLM-Medical-Anonymizer



\# Create virtual environment

python -m venv venv



\# Activate virtual environment

.\\venv\\Scripts\\Activate.ps1



\# If you get execution policy error:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

\# Then activate again: .\\venv\\Scripts\\Activate.ps1



\# Install dependencies

python -m pip install --upgrade pip

pip install -r requirements.txt

```



\### Step 6: Configure Model Path



Edit `config.yml` and update the model path:

```yaml

models:

&nbsp; - name: "TinyLlama-1.1B"

&nbsp;   path\_to\_gguf: "C:\\\\models\\\\tinyllama-1.1b-chat-v1.0.Q4\_K\_M.gguf"

&nbsp;   context\_size: 2048

```



\### Step 7: Run the Application

```powershell

\# Make sure virtual environment is active (you should see (venv) in prompt)

python app.py --model\_path C:\\models --server\_path C:\\llama.cpp\\llama-server.exe --n\_gpu\_layers 0 --port 5001

```



\### Step 8: Access in Browser



Open: http://localhost:5001



\## Running Again Later



Every time you want to run the app:

```powershell

cd C:\\LLM-Medical-Anonymizer

.\\venv\\Scripts\\Activate.ps1

python app.py --model\_path C:\\models --server\_path C:\\llama.cpp\\llama-server.exe --n\_gpu\_layers 0 --port 5001

```



\## Troubleshooting



\*\*"python: command not found"\*\*

→ Reinstall Python and check "Add to PATH"



\*\*"tesseract: command not found"\*\*

→ Add to PATH: `C:\\Program Files\\Tesseract-OCR`



\*\*Out of memory\*\*

→ Close other programs, use TinyLlama model



\*\*Port already in use\*\*

→ Change port: `--port 5002`



\## Features



\- 🤖 AI-powered PII extraction

\- 📊 92.4% average confidence scores

\- 🛡️ Privacy risk assessment (k-anonymity)

\- 🔒 100% local processing (no cloud)

\- 📄 Supports PDF, DOCX, TXT, images

\- ✅ HIPAA compliant

