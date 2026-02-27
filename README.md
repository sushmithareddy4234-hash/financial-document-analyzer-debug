# Financial Document Analyzer – Debug Assignment Solution

---

## 1. Introduction

This project is a **Financial Document Analyzer** built using **FastAPI and CrewAI**.  
The system allows users to upload financial PDF documents and receive structured financial analysis strictly based on the document content.

The original repository contained multiple architectural and configuration issues. These were identified, debugged, and resolved to make the system fully functional.

### Enhancements Implemented

- Background task processing (queue-like behavior)
- SQLite database integration for storing analysis results
- Persistent file-based output storage

The system is now fully functional and stable.

---

# 2. Bugs Identified and Fixes


 Bug 1: Incorrect CrewAI Import

### Issue  
Incorrect import caused:


ImportError: cannot import name 'Agent'

 Fix
```python
from crewai import Agent
```

Bug 2: LLM Provider Not Configured
Issue

LiteLLM error:

LLM Provider NOT provided

Model was passed without specifying provider.

Fix
```python
from crewai import LLM
import os

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
```

Bug 3: Deprecated / Invalid Model Names
Issue

Models like:

llama-3.3-70b

llama-3.3-70b-versatile

Were deprecated or inaccessible.

Fix

Replaced with valid Groq model:
```python
groq/llama-3.1-8b-instant
```

Bug 4: PDF Content Not Passed to Agent
Issue

Uploaded PDF content was not properly extracted and passed to Crew task.

Fix
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(file_path)
docs = loader.load()
full_text = "\n".join([doc.page_content for doc in docs])
document_content = full_text[:3000]
```
This ensures:

Proper document extraction

Token control for faster execution

Bug 5: Blocking API Execution
Issue

The /analyze endpoint blocked execution until analysis completed.
```python
Fix

Implemented FastAPI BackgroundTasks:

background_tasks.add_task(
    process_document,
    job_id,
    query.strip(),
    file_path
)
```
Now:

/analyze returns immediately

Processing runs in background

/result/{job_id} retrieves result

Bug 6: No Result Persistence
Issue

Results were stored only in memory.

Fix

Implemented SQLite database integration using SQLAlchemy.
```python
class JobResult(Base):
    __tablename__ = "job_results"

    job_id = Column(String, primary_key=True, index=True)
    status = Column(String)
    analysis = Column(Text)
```
Results are now:

Stored in results.db

Saved in outputs/{job_id}.txt

3. Setup Instructions (Step-by-Step)
   
Step 1: Clone the Repository
```python
git clone <your-repository-link>
cd financial-document-analyzer-debug
```

Step 2: Create Virtual Environment (Important)
On Windows
```python
python -m venv venv
venv\Scripts\activate
```
On Mac/Linux
```python
python3 -m venv venv
source venv/bin/activate
```

One should now see (venv) in the terminal.

Step 3: Install Dependencies
```python
pip install -r requirements.txt
```

Step 4: Configure Environment Variables

Create a .env file in the project root:
```python

GROQ_API_KEY=your_actual_groq_api_key
```

Step 5: Run the Application
```python
uvicorn main:app --reload
```
Server runs at:
```python
http://127.0.0.1:8000
```
4. How to Use the System
   
Step 1: Open Swagger UI

Go to:
```python
http://127.0.0.1:8000/docs
```

Step 2: Upload Financial PDF (POST /analyze)

Expand POST /analyze

Click Try it out

Upload a financial PDF

Click Execute

Response:
```python
{
  "status": "accepted",
  "job_id": "generated-uuid"
}
```
Copy the job_id.

Step 3: Fetch Result (GET /result/{job_id})

Expand GET /result/{job_id}

Paste the job_id

Click Execute

Possible Responses
Processing
```python
{
  "status": "processing"
}
```
Completed
```python
{
  "status": "completed",
  "analysis": "...",
  "saved_to": "outputs/{job_id}.txt"
}
```
Failed
```python
{
  "status": "failed",
  "error": "error details"
}
```
5. Database Implementation

SQLite database file: results.db

Automatically created on first run

Stores:

job_id

status

analysis result

This ensures persistence even if the server restarts.

6. API Documentation
POST /analyze

Uploads financial PDF and starts background processing.

Request

file (PDF)

query (optional)

Response
```python
{
  "status": "accepted",
  "job_id": "uuid"
}
```
GET /result/{job_id}

Fetch analysis result.

Returns:

processing

completed

failed

7. Bonus Implementations Completed

 Background task queue model
 SQLite database integration
 Output file persistence
 Proper LLM provider configuration
 Structured API documentation

Final Outcome

This solution demonstrates:

Debugging capability

Proper LLM integration (Groq + CrewAI)

API design

Background processing

Database persistence

Clean architecture
