# Pre-loaded Resume Pool (Synthetic Data)

This folder is the app's live resume store — files here are looked up by
`app.py` using the candidate ID stored alongside each embedding in
`resume_db/`. The three PDFs currently in this folder (named by UUID) are
**AI-generated, synthetic resumes** (the same fictional "Arjun Mehta" and
"Daniel Cruz" profiles also included in `data/sample_resumes/`) — no real
person's data is stored here.

Files uploaded through the app's uploader at runtime are also saved to this
folder and indexed into `resume_db/`.
