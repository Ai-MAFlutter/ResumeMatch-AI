# 📄 ResumeMatch AI

## 🚀 AI-Powered Resume Analyzer & ATS Matching System

ResumeMatch AI is an intelligent resume analysis platform that uses **Artificial Intelligence, RAG (Retrieval-Augmented Generation), and Large Language Models** to analyze resumes, compare them with job descriptions, and provide actionable career improvement suggestions.

The system helps candidates understand their resume strength, identify missing skills, and improve their chances of passing ATS (Applicant Tracking Systems).

---

# ✨ Features

## 🎯 ATS Resume Matching

- Calculates Resume Match Score against a Job Description.
- Identifies matching and missing skills.
- Provides an ATS compatibility evaluation.

---

## 🤖 AI Resume Analysis

Using LLM-powered analysis, the system provides:

- Resume strengths.
- Weakness identification.
- Missing skill recommendations.
- Learning roadmap.
- Career improvement suggestions.

---

## 📊 Interactive Dashboard

The application provides visual insights using:

- ATS Gauge Score.
- Skills Comparison Charts.
- Skill Profile Radar Chart.
- Interactive Plotly visualizations.

---

## 💬 AI Resume Assistant

Users can ask questions about their resume:

Examples:

- "What skills should I improve?"
- "How can I increase my ATS score?"
- "Is my resume suitable for this position?"

The assistant answers using the uploaded resume context through a RAG pipeline.

---

## 📄 PDF Report Generation

Automatically generates a professional resume analysis report including:

- ATS Score.
- Matching Skills.
- Missing Skills.
- AI Recommendations.

---

# 🧠 Architecture

The project follows a Retrieval-Augmented Generation (RAG) architecture:

```
Resume PDF
    |
    ↓
PDF Text Extraction
    |
    ↓
Text Cleaning & Chunking
    |
    ↓
Vector / Search Index
    |
    ↓
Relevant Context Retrieval
    |
    ↓
LLM Analysis
    |
    ↓
AI Resume Feedback
```

---

# 🛠️ Technologies Used

## Programming

- Python

## AI & LLM

- Groq API
- LLM Models
- Retrieval-Augmented Generation (RAG)

## Backend / Processing

- Streamlit
- PDF Parsing
- Text Processing

## Data & Visualization

- Plotly
- Pandas

## Development Tools

- Git
- GitHub
- Virtual Environment

---

# 📂 Project Structure

```
ResumeMatch-AI/

│
├── app.py              # Main Streamlit Application
├── rag.py              # RAG and LLM Integration
├── matcher.py          # Resume and Job Matching Logic
├── parser.py           # PDF Extraction
├── search.py           # Search Index
├── chunking.py         # Text Chunking
├── pdf_report.py       # PDF Report Generator
├── utils.py            # Helper Functions
│
├── assets/
│   ├── style.css
│   └── logo.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ResumeMatch-AI.git
```

Navigate to the project folder:

```bash
cd ResumeMatch-AI
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

# ▶️ Run Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open at:

```
http://localhost:8501
```

---

# 📸 Screenshots

(Add your application screenshots here)

---

# 🔮 Future Improvements

Planned features:

- 🌙 Dark / Light Mode
- 🎨 Advanced Glassmorphism UI
- 👤 Automatic Resume Information Extraction
- 📌 Keyword Recommendation System
- 📱 Flutter Mobile Application
- ☁️ Cloud Deployment
- 🔐 User Authentication

---

# 🎯 Learning Outcomes

Through this project, I gained practical experience with:

- Building AI-powered applications.
- Implementing RAG pipelines.
- Working with LLM APIs.
- Prompt Engineering.
- Resume parsing and NLP processing.
- Creating interactive AI dashboards.

---

# 👩‍💻 Author

**Marina Wahid**

AI & Software Developer

---

⭐ If you find this project useful, consider giving it a star!