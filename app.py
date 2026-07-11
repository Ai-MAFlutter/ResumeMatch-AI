import os
import streamlit as st
import plotly.graph_objects as go

from parser import read_pdf
from utils import clean_text
from chunking import split_text
from search import build_index
from pdf_report import generate_report
from rag import analyze_resume, ask_resume
# =====================================================
# ATS GAUGE CHART
# =====================================================

def create_ats_gauge(score):

    if score < 40:
        color = "#EF4444"

    elif score < 70:
        color = "#F59E0B"

    else:
        color = "#22C55E"


    fig = go.Figure(
        go.Indicator(

            mode="gauge+number",

            value=score,

            title={
                "text": "ATS Match Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": color
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#450A0A"
                    },

                    {
                        "range": [40, 70],
                        "color": "#78350F"
                    },

                    {
                        "range": [70, 100],
                        "color": "#064E3B"
                    }

                ]

            }

        )
    )


    fig.update_layout(

        height=350,

        paper_bgcolor="#0F172A",

        font={
            "color":"white"
        }

    )


    return fig
# =====================================================
# SKILLS RADAR CHART
# =====================================================

def create_skill_radar(skill_scores):

    categories = list(skill_scores.keys())

    values = list(skill_scores.values())


    # Close radar shape
    values.append(values[0])
    categories.append(categories[0])


    fig = go.Figure()


    fig.add_trace(

        go.Scatterpolar(

            r=values,

            theta=categories,

            fill="toself",

            name="Skill Level",

            line=dict(
                color="#22C55E",
                width=3
            ),

            marker=dict(
                size=7
            )

        )

    )


    fig.update_layout(

        polar=dict(

            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(

                visible=True,

                range=[0,100],

                tickfont=dict(
                    size=10,
                    color="#64748B"
                )

            ),

            angularaxis=dict(

                tickfont=dict(
                    size=12,
                    color="#1F2937"
                )

            )

        ),


        showlegend=False,


        height=450,


        paper_bgcolor="rgba(0,0,0,0)",


        plot_bgcolor="rgba(0,0,0,0)",


        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),


        font=dict(

            color="#1F2937"

        ),


        title={

            "text": "🧠 Skill Profile",

            "x":0.05,

            "font":{

                "size":20

            }

        }

    )


    return fig
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ResumeMatch AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main{
    background:#f5f7fb;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#1f77ff;
    font-weight:800;
}

[data-testid="stMetricValue"]{
    font-size:34px;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 20px rgba(0,0,0,.08);
}

.upload-box{
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0 3px 15px rgba(0,0,0,.08);
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📄 ResumeMatch AI")

    st.success("AI Powered ATS Resume Analyzer")

    st.write("---")

    st.markdown("""
### Features

✅ ATS Match Score

✅ Resume Analysis

✅ Missing Skills

✅ AI Suggestions

✅ Resume Chat

✅ PDF Report
""")

    st.write("---")

    st.info(
        "Upload your Resume and compare it against any Job Description."
    )

# =====================================================
# HEADER
# =====================================================

st.title("📄 ResumeMatch AI")

st.write(
"""
Analyze your Resume against any Job Description using AI.

Get:

- ATS Match Score
- Missing Skills
- Resume Feedback
- AI Suggestions
- PDF Report
"""
)

st.write("")

# =====================================================
# INPUT SECTION
# =====================================================

left, right = st.columns(2)

with left:

    st.markdown(
        "<div class='upload-box'>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

with right:

    job_description = st.text_area(
        "📋 Paste Job Description",
        height=280,
        placeholder="Paste the job description here..."
    )

st.write("")

# =====================================================
# ANALYZE BUTTON
# =====================================================

if uploaded_file and job_description:

    if st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    ):

        progress = st.progress(0)

        try:

            progress.progress(10)

            temp_path = "temp_resume.pdf"

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            progress.progress(25)

            resume_text = read_pdf(temp_path)

            if len(resume_text.strip()) == 0:

                st.error("No text found inside PDF.")

                st.stop()

            progress.progress(40)

            cleaned = clean_text(resume_text)

            progress.progress(55)

            chunks = split_text(cleaned)

            progress.progress(70)

            index = build_index(chunks)

            progress.progress(85)

            analysis = analyze_resume(
                cleaned,
                job_description
            )

            progress.progress(100)

            st.session_state.analysis = analysis
            st.session_state.index = index
            st.session_state["job_description"] = job_description
            st.session_state["resume_text"] = cleaned

            if os.path.exists(temp_path):
                os.remove(temp_path)

            st.success("✅ Resume analyzed successfully!")

        except Exception as e:

            st.error(e)
            # =====================================================
# RESULTS
# =====================================================

if "analysis" in st.session_state:

    analysis = st.session_state.analysis

    generate_report(
        "Resume_Report.pdf",
        analysis["score"],
        analysis["matching"],
        analysis["missing"],
        analysis["report"]
    )

    st.write("")
    st.divider()

    # ==========================================
    # METRICS
    # ==========================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🎯 ATS Match Score",
            f"{analysis['score']}%"
        )

    with c2:

        st.metric(
            "✅ Matching Skills",
            len(analysis["matching"])
        )

    with c3:

        st.metric(
            "❌ Missing Skills",
            len(analysis["missing"])
        )
    ats_chart = create_ats_gauge(
        analysis["score"]
    )

    st.plotly_chart(
        ats_chart,
        use_container_width=True
    )

    # ==========================================
    # CHARTS
    # ==========================================

    left_chart, right_chart = st.columns(2)

    with left_chart:

        pie = go.Figure()

        pie.add_trace(

            go.Pie(

                labels=[
                    "Matched",
                    "Missing"
                ],

                values=[
                    analysis["score"],
                    100-analysis["score"]
                ],

                hole=.65,

                textinfo="label+percent"

            )

        )

        pie.update_layout(

            title="ATS Resume Match",

            height=450

        )

        st.plotly_chart(

            pie,

            use_container_width=True

        )

    with right_chart:

        bar = go.Figure()

        bar.add_bar(

            name="Matching",

            x=["Skills"],

            y=[len(analysis["matching"])]

        )

        bar.add_bar(

            name="Missing",

            x=["Skills"],

            y=[len(analysis["missing"])]

        )

        bar.update_layout(

            barmode="group",

            title="Skills Comparison",

            height=450

        )

        st.plotly_chart(

            bar,

            use_container_width=True

        )
        # ==========================================
        # RADAR SKILL CHART
        # ==========================================

        st.divider()


        radar = create_skill_radar(

            analysis["skill_scores"]

        )


        st.plotly_chart(

            radar,

            use_container_width=True

        )

    st.divider()

    # ==========================================
    # AI REPORT
    # ==========================================

    st.subheader("📊 AI Resume Analysis")

    st.markdown(

        analysis["report"]

    )

    st.divider()

    # ==========================================
    # MATCHING / MISSING
    # ==========================================

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Matching Skills")

        if analysis["matching"]:

            for skill in analysis["matching"]:

                st.success(skill)

        else:

            st.info("No matching skills found.")

    with right:

        st.subheader("❌ Missing Skills")

        if analysis["missing"]:

            for skill in analysis["missing"]:

                st.error(skill)

        else:

            st.success("No missing skills detected.")
            st.divider()

    # ==========================================
    # DOWNLOAD REPORT
    # ==========================================

    st.subheader("📄 Download Report")

    try:

        with open("Resume_Report.pdf", "rb") as pdf_file:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="Resume_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    except FileNotFoundError:

        st.warning("PDF report is not available.")

    st.divider()

    # ==========================================
    # ASK AI ABOUT RESUME
    # ==========================================

    st.subheader("💬 Ask AI About Your Resume")

    st.write(
        "Ask any question about your resume, strengths, weaknesses, or how to improve it."
    )

    question = st.text_input(
        "Your Question",
        placeholder="Example: What skills should I improve for this job?"
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if question.strip():

            with st.spinner("Thinking..."):

                try:

                    answer = ask_resume(
                    question,
                    st.session_state["index"],
                    st.session_state.get("job_description", "")
                )

                    st.success("Answer")

                    st.markdown(answer)

                except Exception as e:

                    st.error(f"Error: {e}")

        else:

            st.warning("Please enter a question.")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
<div class="footer">

<b>ResumeMatch AI</b><br>

Built with ❤️ using

<b>Python</b> •
<b>Streamlit</b> •
<b>Groq LLM</b> •
<b>RAG</b> •
<b>Plotly</b>

</div>
""",
    unsafe_allow_html=True
)
