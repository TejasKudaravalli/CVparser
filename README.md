# CVparser

CVparser is an **asynchronous Resume Parser API** built with **FastAPI**.  
It automatically **extracts and structures key information from ATS freindly resumes** using **pure NLP techniques**, outputting the data in a clean JSON format.

---

## 🚀 Features

- Upload and parse individual resumes **synchronously** or **asynchronously**.
- **Batch parsing** for multiple resumes at once.
- **Supported file types**: `.pdf`, `.docx`, `.rtf`, `.txt`
- Extracted information includes:
  - **Basic Information** (Name, Email, Phone, etc.)
  - **Education Details**
  - **Language Proficiencies**
  - **Professional Experiences**
  - **Awards and Honors**
  - **Trainings and Certifications**
  - **References**

---

## 📂 Project Structure

```bash
.
├── src/
│   └── nlp  # Core NLP-based resume parsing logic
├── uploads/                              # Temporary storage for uploaded files
├── main.py                               # FastAPI application
└── README.md                             # Project documentation
```

---

## 📜 API Endpoints

### 1. Parse Resume (Synchronous)

- **Endpoint**: `POST /parse-resume/`
- **Description**: Upload a single resume and receive the parsed JSON immediately.
- **Request**: `UploadFile`
- **Response**:
  ```json
  {
    "basic": { ... },
    "education": [ ... ],
    "languages": [ ... ],
    "professional_experiences": [ ... ],
    "awards": [ ... ],
    "trainings_and_certifications": [ ... ],
    "references": [ ... ]
  }
  ```

---

### 2. Parse Resume (Asynchronous)

- **Endpoint**: `POST /parse-resume-async/`
- **Description**: Upload a single resume and process it in the background.
- **Request**: `UploadFile`
- **Response**:
  ```json
  {
    "task_id": "uuid-generated-task-id"
  }
  ```

- **Check Status**:  
  - **Endpoint**: `GET /parse-result/{task_id}`
  - **Responses**:
    ```json
    { "status": "in_progress" }
    ```
    or
    ```json
    { "status": "completed", "result": { ... } }
    ```

---

### 3. Batch Parse Resumes

- **Endpoint**: `POST /parse-resume-batch/`
- **Description**: Upload multiple resumes at once for batch processing.
- **Request**: `List[UploadFile]`
- **Response**:
  ```json
  {
    "results": [
      { "filename": "resume1.pdf", "data": { ... } },
      { "filename": "resume2.docx", "data": { ... } },
      ...
    ]
  }
  ```

---

## ⚙️ How it Works

1. The uploaded file is saved temporarily to a local `uploads/` directory.
2. The file is passed through a custom **NLP-based extraction pipeline** (`extract_json_from_resume_nlp`).
3. Structured data is generated under the following fields:
   - `basic`
   - `education`
   - `languages`
   - `professional_experiences`
   - `awards`
   - `trainings_and_certifications`
   - `references`
4. The result is returned as JSON.

---

## 🛠️ Run Locally

1. **Install dependencies**:
    ```bash
    uv pip install .
    ```

2. **Start the server**:
    ```bash
    python main.py
    ```

3. **Access the API docs**:
    - Interactive Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📢 Notes

- Only `.pdf`, `.docx`, `.rtf`, and `.txt` files are supported.
- Uploaded files are stored temporarily in the `uploads/` directory.
- Be sure to implement file cleanup strategies in production environments.
- Current parsing is based purely on NLP techniques — no template matching or external parsing libraries are used.