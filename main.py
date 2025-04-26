from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
from pathlib import Path
import aiofiles
import asyncio
import uuid

from src import extract_json_from_resume_nlp

app = FastAPI(title="Resume Parser API (Asyncio)")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".rtf", ".txt"}

# In-memory store for async tasks and results
parse_tasks: Dict[str, asyncio.Task] = {}
parse_results: Dict[str, Dict] = {}


# Utility to save uploaded file
async def save_file(file: UploadFile) -> str:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    
    file_id = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / file_id
    
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return str(file_path)

# Background task function
async def parse_resume_background(task_id: str, file_path: str):
    result = extract_json_from_resume_nlp(file_path)
    parse_results[task_id] = result

# Async background parsing
@app.post("/parse-resume-async/")
async def parse_resume_async(file: UploadFile = File(...)):
    file_path = await save_file(file)
    task_id = str(uuid.uuid4())
    task = asyncio.create_task(parse_resume_background(task_id, file_path))
    parse_tasks[task_id] = task
    return {"task_id": task_id}

# Check task result
@app.get("/parse-result/{task_id}")
async def get_parse_result(task_id: str):
    task = parse_tasks.get(task_id)
    if not task:
        return {"status": "not_found"}
    if not task.done():
        return {"status": "in_progress"}
    return {"status": "completed", "result": parse_results.get(task_id)}

# Sync parsing
@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    file_path = await save_file(file)
    result = extract_json_from_resume_nlp(file_path)
    return JSONResponse(content=result)

# Batch parsing
@app.post("/parse-resume-batch/")
async def parse_resume_batch(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            file_path = await save_file(file)
            result = extract_json_from_resume_nlp(file_path)
            results.append({"filename": file.filename, "data": result})
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})
    return JSONResponse(content={"results": results})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)