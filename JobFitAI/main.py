import streamlit as st
from datetime import datetime
import urllib.parse
from JobFitAI.supabase_utils import upload_pdf_to_supabase, insert_resume_data
from JobFitAI.utils import ExtractPDF, SendRequest, CreatePDF

def JobFitAI():
    st.title("JobFitAI: AI-Powered Resume Optimization")

    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Enter the Job Description", height=200)

    if uploaded_file and job_description:
        resume_text = ExtractPDF(uploaded_file)

        if st.button("Optimize"):
            optimized_text = SendRequest("Optimisation-Prompt.txt", resume_text)
            st.text_area("Optimized Resume", optimized_text, height=300)

            # Create in-memory PDF
            pdf_file = CreatePDF(optimized_text)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{uploaded_file.name.replace('.pdf', '')}_Optimized_{timestamp}.pdf"

            # Upload PDF to Supabase
            upload_result = upload_pdf_to_supabase(pdf_file.getvalue(), file_name)

            if upload_result:
                insert_resume_data(
                    filename=file_name,
                    original=resume_text,
                    optimized=optimized_text,
                    jd=job_description
                )

                st.success("Resume optimized and uploaded to Supabase successfully!")

                encoded_file_name = urllib.parse.quote(file_name)
                public_url = f"{st.secrets['SUPABASE_URL']}/storage/v1/object/public/resumes/{encoded_file_name}"
                st.markdown(f"[📄 Download Optimized Resume]({public_url})", unsafe_allow_html=True)
            else:
                st.error("PDF upload failed. Please try again.")

def ATSAnalysis():
    st.title("JobFitAI: ATS Score Analysis")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Enter the Job Description", height=200)
    
    if uploaded_file is not None and job_description:
        if st.button("Analyze ATS Score"):
            resume_data = ExtractPDF(uploaded_file)
            req_text = "Resume: " + resume_data + "\nJob Description: " + job_description
            ats_result = SendRequest("ATS_Check.txt", req_text)
            st.text_area("ATS Score Result", ats_result, height=500)


def SkillsAnalysis():
    st.title("JobFitAI: Skills Analysis")
    job_description = st.text_area("Enter the Job Description", height=200)
    if st.button("Analyze Keywords"):
        if job_description:
            analysis_result = SendRequest("Keyword_Prompt.txt", job_description)
            st.subheader("Skills Categorized from Job Description")
            st.text_area("", analysis_result, height=200)
        else:
            st.error("Please enter a job description to analyze.")

def BulletPointAnalysis():
    st.title("JobFitAI: Bullet Point Optimization")
    bullet_ = st.text_area("Enter Your Bullet Point", height=100)   
        
    if st.button("Analyze Bullet Points"):
        if bullet_:
            bullet_analysis = SendRequest("Bullet_Prompt.txt", bullet_)
            st.text_area("Optimized Bullet Points", bullet_analysis, height=150)
        else:
            st.error("Please Enter a Bullet Point to Analyze.")

def MetricAnalysis():
    st.title("JobFitAI: Metric Analysis")
    bullet = st.text_area("Enter Your Bullet Point", height=100)
    if st.button("Analyze"):
        if bullet:
            metric_result = SendRequest("Metric_Prompt.txt", bullet)
            st.text_area("Metric Result", metric_result, height=300)