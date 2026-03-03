# Financial Document Analyzer – Debug Assignment

## Bugs Found & Fixes

### 1. Dependency Conflicts
- `pydantic==1.x` conflicted with `crewai==0.130.0` (requires v2).
- `openai` and `fastapi` versions were incompatible with CrewAI dependencies.
**Fix:** Upgraded to compatible versions and removed restrictive pins.  
**Result:** Clean installation and stable environment.

---

### 2. Broken PDF Loader
- Used undefined `Pdf()` class → runtime crash.
**Fix:** Replaced with `PyPDFLoader`.  
**Result:** Stable PDF parsing.

---

### 3. No Financial Document Validation
- System accepted any PDF.
**Fix:** Added deterministic keyword-based financial validation.  
**Result:** Prevents non-financial document analysis.

---

### 4. Inefficient Prompts
- Tasks were vague and unstructured.
**Fix:** Added step-by-step instructions and enforced structured JSON output.  
**Result:** Consistent, reliable responses.

---

### 5. Weak Verifier Agent
- No measurable validation criteria.
**Fix:** Verifier now checks:
- JSON structure
- Logical consistency
- Compliance

---

### 6. Unsafe File Handling
- Used original filename → overwrite risk.
**Fix:** Switched to UUID-based temporary filenames.

---

### 7. No Concurrency Handling
- Original system was synchronous and blocking.
**Fix:**
Added Celery + Redis queue worker.
Background job processing.
Status tracking endpoint.

---

### 8. No Persistence Layer
- Results were ephemeral.
**Fix:**
Integrated SQLite via SQLAlchemy.
Stored job status and result.
Added /status/{job_id} endpoint.

---

### 9. No Logging / Observability
- No structured visibility into task state.
**Fix:**
Verbose Crew logs enabled
Explicit status tracking via DB
Failure state stored and returned

---

### 10. No Structured Output Contract
- Original output was free-form text.
**Fix:** Enforced strict JSON schema and added expected output format inside tasks.

---

## Setup Instructions

### Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create .env File
```bash
OPENAI_API_KEY=your_key
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///./analysis.db
```

### Start Redis
```bash
docker run -d -p 6379:6379 redis
```

### Start Celery Worker
```bash
celery -A worker.celery worker --loglevel=info
```

### Start API
```bash
uvicorn main:app --reload
```

### Open in browser:
http://127.0.0.1:8000/docs


## API Documentation

### POST /analyze
Uploads financial PDF and creates async job.
Fields:
file (PDF)
query (string)
Response:
```json
{
  "job_id": "uuid",
  "status": "PENDING"
}
```
### GET /status/{job_id}
Returns job status and result.
Response (Success):
```json
{
  "job_id": "uuid",
  "status": "SUCCESS",
  "result": "{ structured JSON output }"
}
```
