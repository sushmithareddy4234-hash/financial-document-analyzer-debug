# Financial Document Analyzer – Debug Assignment

## Project Overview

This project is an AI-powered financial document analysis system built using CrewAI and FastAPI.

The system processes uploaded financial PDF documents and generates structured financial insights including:

- Financial highlights  
- Revenue and profitability analysis  
- Risk assessment  
- Investment outlook  
- Document limitations  

The application uses background processing and database persistence to handle asynchronous analysis jobs efficiently.


## Tech Stack

- FastAPI (API framework)
- CrewAI (Agent orchestration)
- Groq LLM (llama-3.1-8b-instant)
- SQLAlchemy (SQLite database)
- LangChain PDF Loader
- Background task processing (non-blocking queue simulation)


## Setup Instructions

### 1. Create Virtual Environment

python -m venv venv  
venv\Scripts\activate  


### 2. Install Dependencies

pip install -r requirements.txt  


### 3. Configure Environment Variables

Create a `.env` file in the root directory:

GROQ_API_KEY=your_groq_api_key_here  


## Running the Application

python -m uvicorn main:app --reload  

Server will run at:

http://127.0.0.1:8000  


## API Endpoints

### POST /analyze

Upload a PDF file for financial analysis.

Form Data:
- file: PDF document
- query: Optional analysis instruction

Response:
- job_id (used to fetch results)


### GET /result/{job_id}

Fetch analysis result for a submitted job.


## Database

Results are stored in:

results.db  

Each job stores:
- job_id
- status
- analysis output


## Key Improvements Made

- Fixed CrewAI agent initialization errors  
- Corrected LLM provider configuration  
- Resolved PDF loading bugs  
- Implemented background task processing  
- Added SQLite database persistence  
- Cleaned inefficient prompts  
- Limited token size for performance optimization  
- Added proper error handling  


## Supported File Type

- PDF only


## Project Status

Fully functional and tested.