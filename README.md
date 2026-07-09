# Talent Fit - AI Resume Ranker

An AI-powered resume ranking system with intelligent evaluation, semantic search, and a Streamlit web interface.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# then edit .env and fill in your Azure OpenAI endpoint/key

# 3. Run the app
streamlit run app.py
```
Access at: http://localhost:8501

## Architecture Overview

- **Frontend**: Streamlit web application
- **AI Engine**: Azure OpenAI (GPT-4o + text-embedding-ada-002)
- **Vector Database**: ChromaDB for semantic resume search
- **Storage**: SQLite (via ChromaDB) for embeddings and metadata
- **Processing**: PDF parsing and contact extraction

## Project Structure

```
├── app.py                     # Main Streamlit application
├── custom_rag.py               # Core RAG implementation
├── llm_interface.py            # Azure OpenAI integration
├── vector_db.py                 # Vector database operations
├── config_loader.py            # Configuration management
├── config/config.yaml          # App/LLM configuration (no secrets)
├── Testing/                    # Jupyter notebooks for manual testing
├── data/sample_resumes/        # Synthetic sample resumes for demos
├── resumes/                    # Live resume pool used by the running app
├── resume_db/                  # ChromaDB persistent vector store
├── prompts/                    # LLM prompt templates
└── .env.example                # Template for required environment variables
```

## Core Features

### 1. AI-Powered Evaluation
- Multi-criteria evaluation (Technical Skills, Experience, Education, Leadership, etc.)
- Evidence-based scoring with AI-generated reasoning
- Weighted scoring, customizable per job description

### 2. Web Interface
- Upload resumes (PDF/DOCX) into a searchable pool
- Enter a job description and rank the pool against it
- Expandable per-candidate detail view with score breakdown and evidence

### 3. Semantic Search
- ChromaDB vector embeddings for resume matching
- Persistent storage across sessions
- Contact info (name/email/phone) extraction

## Configuration

Credentials are never stored in the repo. Set them via environment variables
(see `.env.example`), or via Streamlit secrets (`.streamlit/secrets.toml`,
which is gitignored) when deploying to Streamlit Cloud:

```
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Non-secret app settings (model name, token limits, job description templates)
live in `config/config.yaml`.

## Sample / Demo Data

`data/sample_resumes/` and the pre-loaded contents of `resumes/` are
**entirely synthetic, AI-generated resumes** — fictional names, emails, and
work histories used only to demo the app. See
[`data/sample_resumes/README.md`](data/sample_resumes/README.md) for details.

## Testing

Manual/exploratory test notebooks live in `Testing/`:
- `custom_rag_test.ipynb` — RAG system validation
- `vector_db_test.ipynb` — database operations
- `llm_test.ipynb` — Azure OpenAI integration

## Use Cases

- HR teams screening high volumes of resumes against a role
- Recruitment agencies ranking candidates for client requirements
- Technical hiring teams doing AI-assisted first-pass evaluation
