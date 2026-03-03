from fastapi import FastAPI, UploadFile, File, Form
from crewai import Crew, Process
import uuid
from tasks import (
    analyze_document,
    assess_risk,
    advise_investment,
    verify_output
)
import shutil
import os

app = FastAPI()


@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed."}

    unique_id = str(uuid.uuid4())
    file_path = f"temp_{unique_id}.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        crew = Crew(
            agents=[
                analyze_document.agent,
                assess_risk.agent,
                advise_investment.agent,
                verify_output.agent
            ],
            tasks=[
                analyze_document,
                assess_risk,
                advise_investment,
                verify_output
            ],
            process=Process.sequential
        )

        result = crew.kickoff({
            "query": query,
            "path": file_path
        })

        return {"result": str(result)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)