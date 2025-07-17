import os
import time
import streamlit as st
from fpdf import FPDF
from PyPDF2 import PdfReader
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv('.env')
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
st.write("API key loaded:", GOOGLE_API_KEY is not None)
if GOOGLE_API_KEY:
 genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("key not found")
    st.stop()
# Function to Extract Text from PDF
def ExtractPDF(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to Optimize Resume Text using Google Gemini API
def SendRequest(prompt_filename, user_text):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    try:
        with open(f"Prompts/{prompt_filename}", "r") as file:
            prompt_template = file.read()
    except FileNotFoundError:
        st.error(f" Missing prompt file: {prompt_filename}")
        return ""

    full_prompt = prompt_template + "\n" + user_text

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            if "quota" in str(e).lower() or "ResourceExhausted" in str(e):
                st.warning(f"Quota exhausted. Retrying in 60s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(60)
            else:
                raise e

    # If all retries fail
    st.error("Google Gemini API quota is exhausted. Please try again later or check your billing/quota.")
    return "Quota exceeded. Resume not optimized."




# Function to create a PDF with optimized resume
def CreatePDF(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_margins(10, 10, 10)
    pdf.set_font("Courier", size=10)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), align='L')
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_bytes)