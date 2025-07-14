import streamlit as st
api_key = st.secrets["GOOGLE_API_KEY"]

from JobFitAI.main import *

# Page Configurations
st.set_page_config(page_title="JobFitAI: AI-Powered Resume Optimizer", page_icon="⭐")
st.sidebar.title("JobFitAI - Tools")
page = st.sidebar.selectbox(
    "Select an option",
    ["Resume Optimisation", "Bullet-Point Analysis", "Know the Needed Skills", "ATS Score Analysis", "Metric Analytics"]
)


# Loading CSS for the app
@st.cache_data
def load_css():
    with open("static/styles.css") as f:
        return f.read()
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

if page == "Resume Optimisation":
    JobFitAI()
elif page == "Bullet-Point Analysis":
    BulletPointAnalysis()
elif page == "Know the Needed Skills":
    SkillsAnalysis()
elif page == "ATS Score Analysis":
    ATSAnalysis()
elif page == "Metric Analytics":
    MetricAnalysis()