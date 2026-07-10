import streamlit as st

from parser import read_pdf
from utils import clean_text
from chunking import split_text
from search import build_index

from rag import analyze_resume, ask_resume
from matcher import compare_skills



st.set_page_config(
    page_title="ResumeMatch AI",
    page_icon="📄",
    layout="wide"
)



st.title("📄 ResumeMatch AI")

st.write(
    "Upload your resume, paste the job description, and let AI analyze your match."
)


st.divider()



uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)



job_description = st.text_area(
    "Paste Job Description",
    height=250
)



if uploaded_file is not None and job_description:


    if st.button("🚀 Analyze Resume"):


        with st.spinner("Processing Resume..."):


            # Save uploaded PDF
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())



            # Extract text from PDF
            text = read_pdf(
                "temp_resume.pdf"
            )



            # Clean text
            cleaned = clean_text(
                text
            )



            # Split into chunks
            chunks = split_text(
                cleaned
            )



            # Create search index for RAG
            index = build_index(
                chunks
            )



            # Generate AI analysis
            analysis = analyze_resume(
                cleaned,
                job_description
            )



            # Save data in session
            st.session_state["analysis"] = analysis

            st.session_state["index"] = index



        st.success(
            "Analysis Complete!"
        )





# ==========================
# Display Results
# ==========================


if "analysis" in st.session_state:


    analysis = st.session_state["analysis"]



    st.divider()


    st.subheader(
        "🎯 Resume Match Score"
    )



    score = analysis["score"]



    st.progress(
        score / 100
    )



    st.metric(
        "Match Score",
        f"{score}%"
    )



    st.divider()



    st.subheader(
        "📊 AI Resume Analysis"
    )



    st.markdown(
        analysis["report"]
    )



    st.divider()



    # ==========================
    # Skills Section
    # ==========================


    col1, col2 = st.columns(2)



    with col1:

        st.subheader(
            "✅ Matching Skills"
        )


        for skill in analysis["matching"]:

            st.write(
                f"✔️ {skill}"
            )



    with col2:

        st.subheader(
            "❌ Missing Skills"
        )


        for skill in analysis["missing"]:

            st.write(
                f"⚠️ {skill}"
            )



    st.divider()



    # ==========================
    # Ask AI
    # ==========================


    st.subheader(
        "💬 Ask AI About Your Resume"
    )



    question = st.text_input(
        "Ask any question about your resume"
    )



    if st.button("Ask AI"):


        if question:


            with st.spinner(
                "Thinking..."
            ):


                answer = ask_resume(
                    question,
                    st.session_state["index"]
                )



            st.success(
                "Done!"
            )



            st.markdown(
                answer
            )



        else:


            st.warning(
                "Please enter a question."
            )