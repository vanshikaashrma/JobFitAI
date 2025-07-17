
from supabase import create_client, Client
import os
import streamlit as st

#  Load Supabase credentials from Streamlit secrets or environment variables
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf_to_supabase(file_data, filename):
    """
    Uploads a PDF file to the Supabase storage bucket named 'resumes'.
    """
    try:
        result = supabase.storage.from_("resumes").upload(
    path=filename,
    file=file_data,
    file_options={"content-type": "application/pdf"}
)

        return result
    except Exception as e:
        st.error(f"Failed to upload PDF to Supabase: {str(e)}")
        return None

def insert_resume_data(filename, original, optimized, jd):
    """
    Inserts resume data into the Supabase 'resumes' table.
    """
    try:
        data = {
            "filename": filename,
            "original_text": original,
            "optimized_text": optimized,
            "job_description": jd
        }
        result = supabase.table("resumes").insert(data).execute()
        return result
    except Exception as e:
        st.error(f"Failed to insert resume data: {str(e)}")
        return None
