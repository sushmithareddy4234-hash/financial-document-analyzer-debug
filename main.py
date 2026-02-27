from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from typing import Dict
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document
from database import SessionLocal, JobResult
from langchain_community.document_loaders import PyPDFLoader

app = FastAPI(title="Financial Document Analyzer")

# In-memory job tracker (queue simulation)
job_store: Dict[str, dict] = {}


def run_crew(query: str, file_path: str):
    """Run CrewAI analysis"""

    # Load PDF properly
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    full_text = "\n".join([doc.page_content for doc in docs])
    document_content = full_text[:3000]  # limit tokens

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "document": document_content
    })

    try:
        return result["tasks_output"][0]["raw"]
    except:
        return str(result)


# Background worker
def process_document(job_id: str, query: str, file_path: str):
    try:
        result = run_crew(query=query, file_path=file_path)

        # Save file output
        os.makedirs("outputs", exist_ok=True)
        output_path = f"outputs/{job_id}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        # Save to database
        db = SessionLocal()
        db_result = JobResult(
            job_id=job_id,
            status="completed",
            analysis=result
        )
        db.add(db_result)
        db.commit()
        db.close()

        job_store[job_id] = {
            "status": "completed",
            "analysis": result,
            "saved_to": output_path
        }

    except Exception as e:
        db = SessionLocal()
        db_result = JobResult(
            job_id=job_id,
            status="failed",
            analysis=str(e)
        )
        db.add(db_result)
        db.commit()
        db.close()

        job_store[job_id] = {
            "status": "failed",
            "error": str(e)
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    job_id = str(uuid.uuid4())
    file_path = f"data/{job_id}.pdf"

    os.makedirs("data", exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    job_store[job_id] = {"status": "processing"}

    background_tasks.add_task(
        process_document,
        job_id,
        query.strip(),
        file_path
    )

    return {
        "status": "accepted",
        "job_id": job_id,
        "message": "Processing started. Use /result/{job_id} to fetch result."
    }


@app.get("/result/{job_id}")
async def get_result(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_store[job_id]


@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}