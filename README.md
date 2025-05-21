# 🛠️ AutoSRE - Incident Analyzer

**AutoSRE** is an intelligent Site Reliability Engineering (SRE) assistant that helps automate root cause analysis, retrieve similar incidents, and suggest resolution steps — all powered by LLMs and vector search. Built with a modular architecture using Streamlit, LangChain, HuggingFace, ChromaDB, and LLaMA 3 via Ollama.

---

## Features 

- **LLM-Based Root Cause Analysis**
- **Contextual Similar Incident Retrieval**
- **Automated Resolution Suggestions**
- **Fast Local Inference with Ollama**
- **Modular Design with Streamlit UI**

---

## Input & Output

- **Input**: Incident Summary / Error / StackTrace
- **Output**: Root Cause, Similar Incidents, Recommended Resolution

---

## Architecture Design

### 1. UI Layer (Frontend)

- **Framework**: Streamlit
- **Responsibilities**:
  - Collect user input
  - Trigger backend logic on button click
  - Display root cause, similar incidents, and resolutions

### 2. Application Layer

- **Chains**:
  - `root_cause_chain`: Summary → Root Cause
  - `responder_chain`: Summary + Root Cause → Resolution
- **Functions**:
  - `analyze_root_cause()`
  - `generate_resolution()`
  - `get_similar_incidents()`

### 3. Backend Layer

- **LLM**: LLaMA 3 via `OllamaLLM`
- **Framework**: LangChain
- **Responsibilities**:
  - Use prompt templates for structured interaction
  - Perform reasoning with LLMs

### 4. Vector Database Layer

- **Embedding Model**: `all-MiniLM-L6-v2` (HuggingFace)
- **Vector Store**: ChromaDB (`data/chroma_db`)
- **Responsibilities**:
  - Embed incident descriptions
  - Perform similarity search over incident history

### 5. Storage Layer

- **Database**: Persistent Chroma DB
- **Stores**: Incident embeddings and metadata

---

## Design Flow

1. **User Input** via Streamlit UI
   - Incident summary, error, or stack trace

2. **Root Cause Analysis**
   - LangChain prompt sent to LLaMA 3 using Ollama
   - Returns a probable root cause

3. **Similar Incidents Retrieval**
   - Input embedded via HuggingFace model
   - Query searched in ChromaDB
   - Returns top K matches

4. **Resolution Generation**
   - Prompt combines summary + root cause
   - LLM returns structured resolution steps

5. **Display Results**
   - Shows root cause, related incidents, and resolution steps

---

## Setup Instructions
### 1. Install Python for Windows   
Go to https://www.python.org/downloads/windows/ and download Python for windows. Recommended version is 3.11.7
#### Check Python version
```bash
python --version    #This should show Python 3.11.7 or above
```

### 2. Install Ollama for Windows  
Go to https://ollama.com/download and download Ollama for Windows. Recommended version is 0.6.6  
Install Ollama
#### Verify the installed version 
```bash
ollama --version    #This will show ollama version 0.6.6
```
#### Verify if Ollama is running 
```bash
PS C:\YOUR-PROJECT-DIRECTORY\AutoSRE> curl http://localhost:11434/  
```
It will show below output:  
```bash
StatusCode        : 200
StatusDescription : OK
Content           : Ollama is running
RawContent        : HTTP/1.1 200 OK
```

### 3. Clone the Repository  
Open windows Powershell  

```bash
cd C:\YOUR-PROJECT-DIRECTORY  
git clone https://github.com/mazo-dev/AutoSRE.git
cd AutoSRE
```
You will see below directory structure  
```bash
C:\YOUR-PROJECT-DIRECTORY\AutoSRE
/data  
/images  
/logs  
/models  
/results  
/src  
README.md  
requirements.txt  
```

### 4. Pull llama3 model
```bash
PS cd C:\YOUR-PROJECT-DIRECTORY\AutoSRE
PS C:\YOUR-PROJECT-DIRECTORY\AutoSRE> ollama pull llama3
pulling manifest
pulling 6a0746a1ec1a... 100% ▕████████████████████████████████████████████████████████▏ 4.7 GB
pulling 4fa551d4f938... 100% ▕████████████████████████████████████████████████████████▏  12 KB
pulling 8ab4849b038c... 100% ▕████████████████████████████████████████████████████████▏  254 B
pulling 577073ffcc6c... 100% ▕████████████████████████████████████████████████████████▏  110 B
pulling 3f8eb4da87fa... 100% ▕████████████████████████████████████████████████████████▏  485 B
verifying sha256 digest
writing manifest
success
PS C:\YOUR-PROJECT-DIRECTORY\AutoSRE>
```
### 5. Create a Python Virtual Environment
Execute below commands
```bash
cd C:\YOUR-PROJECT-DIRECTORY\AutoSRE   
python -m venv myenv  
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  
.\myenv\Scripts\Activate.ps1
(myenv) PS C:\Applications\Workspace\AutoSRE>
```
### 6. Install required Python Libraries 
```bash
pip install -r requirements.txt     #requirement.xt contains all required python libraries for this project
```

### 7. Populate ChromaDB with past incidents
#### Install DB Browser for SQLite  
https://sqlitebrowser.org/dl/  
Sample past incidents are located @ C:\YOUR-PROJECT-DIRECTORY\AutoSRE\data\it_incident_dataset_2000.json  

Execute below python program to load the incidents in ChromaDB
```bash
python src/store_incidents.py
```
### 8. Run the Application with GUI using Streamlite
```bash
PS C:\YOUR-PROJECT-DIRECTORY\AutoSRE>streamlite run .\src\auto_sre_streamlit.py
```
Enter the Incident summary /stacktrace / exception and click "Analyze Incident"

### 9. Run the Application with CLI
```bash
PS C:\YOUR-PROJECT-DIRECTORY\AutoSRE>streamlite run .\src\auto_sre.py
```
Paste the incident summary /stacktrace / exception and hit enter

### 9. Contact Information
If you have any questions, feel free to [email me](mailto:mazodev@gmail.com).
