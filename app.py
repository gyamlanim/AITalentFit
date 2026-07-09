import pysqlite3 as sqlite3
import sys
sys.modules["sqlite3"] = sqlite3
print("sqlite3 module version:", sqlite3.version)
print("SQLite engine version:", sqlite3.sqlite_version)
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from custom_rag import CustomRAG
import os
import mimetypes
import base64


rag_object = CustomRAG(db_path="resume_db", table_name="resume_table")


# Make two columns
col1, col2 = st.columns([1, 12])  # adjust width ratio

with col1:
    st.image("img/logo.png", width=50)  # your logo file

with col2:
    st.markdown(
        "<font style='margin-top:0;font-size:30px'>Talent Fit</font>",
        unsafe_allow_html=True
    )

st.markdown("### Upload more resumes to the Resume pool")
st.caption("Accepted formats: PDF or DOCX.")

# Use session state to prevent multiple uploads
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = set()

uploaded = st.file_uploader("Click below to upload a file", type=None, accept_multiple_files=False, label_visibility="collapsed")

if uploaded and uploaded.name not in st.session_state.uploaded_files:
    result = rag_object.enter_resume_to_db_save_file(uploaded.getbuffer(), uploaded.name)
    st.session_state.uploaded_files.add(uploaded.name)
    st.success(result)

st.markdown("### Find top matching profiles from the Resume pool")
# Textbox for input
user_query = st.text_area(
    "Enter detailed Job description:",
    height=200,  # adjust box height (in pixels)
    placeholder="Paste or type the full job description here..."
)

# Button to trigger the search
if st.button("Find matching resumes"):
    if user_query.strip():
        with st.spinner(" Finding matches..."):
            results = rag_object.evaluate_top_resumes(user_query, 5)
            # Sort resumes by score (highest first)
            results = sorted(results, key=lambda r: r['evaluation']['total_weighted_score'], reverse=True)
        st.success("Results:")
        for res in results:
            # Create two columns: details (left) and score (right)
            col1, col2 = st.columns([3, 1])  # wider left, smaller right

            with col1:
                st.markdown(
                    f"""
                    **Name:** {res['name']}  
                    **Email:** {res['email']}  
                    **Phone:** {res['phone']}
                    """,
                    unsafe_allow_html=True
                )

                file_path = f"resumes/{res['candidate_id']}"

                if os.path.exists(file_path + ".pdf"):
                    file_path += ".pdf"
                elif os.path.exists(file_path + ".docx"):
                    file_path += ".docx"
                else:
                    st.error("❌ File not found.")
                
                # Infer MIME type automatically (falls back to octet-stream if unknown)
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type is None:
                    mime_type = "application/octet-stream"

                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        data = f.read()

                    # Encode to base64 so it works in an <a href="...">
                    b64 = base64.b64encode(data).decode()
                    file_name = os.path.basename(file_path)

                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}"><button style="background-color:#FFFFFF;color:#2E86C1;border:solid 1px #2E86C1;padding:5px 5px;border-radius:5px;cursor:pointer;">⬇️ Download Resume</button></a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("File not found.")

            with col2:
                st.markdown(
                    f"""
                    <div style='text-align:center; 
                                font-size:36px; 
                                font-weight:bold; 
                                color:#2E86C1; 
                                border:2px solid #2E86C1; 
                                border-radius:10px; 
                                padding:10px;'>
                        {res['evaluation']['total_weighted_score']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with st.expander("Show details", expanded=False):
                evaluation = res.get("evaluation", {})
                criteria_scores = evaluation.get("criteria_scores", {})

                st.markdown("#### Strengths:")
                st.write(", ".join(evaluation.get("key_strengths", [])))

                st.markdown("#### Weaknesses:")
                st.write(", ".join(evaluation.get("areas_of_concern", [])))

                st.markdown("---")

                for criteria_score in criteria_scores:
                    # First row: Criterion
                    st.markdown(f"**Criterion:** {criteria_score.get('criterion', '')}")

                    # Second row: Evidence
                    st.markdown(f"**Evidence:** {criteria_score.get('evidence', '')}")

                    # Third row: three columns (score, weight, weighted score)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("**Score**")
                        st.write(criteria_score.get("score", 0))
                    with col2:
                        st.markdown("**Weight**")
                        st.write(criteria_score.get("weight", 0))
                    with col3:
                        st.markdown("**Weighted Score**")
                        st.write(criteria_score.get("weighted_score", 0))
                    st.markdown("---")


            st.markdown("---")  # separator line between resumes
    else:
        st.warning("⚠️ Please enter some text before searching.")