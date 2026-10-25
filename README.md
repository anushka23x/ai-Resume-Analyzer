# 🤖 AI Resume Analyzer

<p align="center">
  <b>AI-Powered Resume Analysis & Job Matching Platform</b>
</p>

<p align="center">
  Analyze your resume • Match job descriptions • Discover missing skills • Improve your career profile
</p>

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![NLP](https://img.shields.io/badge/NLP-Semantic%20Analysis-purple?style=for-the-badge)](https://www.nltk.org/)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](#license)

</p>

---

## 🌐 Live Demo

<p align="center">

### 🚀 Try the AI Resume Analyzer

👉 **[Launch AI Resume Analyzer](https://ai-resume-analyzer-en7y4od9e9owns7usjqtnu.streamlit.app/)**

</p>

---

## 📌 About The Project

**AI Resume Analyzer** is an intelligent web application designed to analyze resumes against specific job descriptions using Natural Language Processing (NLP), machine learning, semantic similarity, and skill-matching techniques.

The application helps students, freshers, developers, and job seekers understand:

- 🎯 How closely their resume matches a job
- 📊 Their ATS compatibility score
- ✅ Which skills they already have
- ❌ Which skills may be missing
- 🔑 Which keywords are important
- 💡 How their resume can be improved
- 🚀 Which job roles may suit their profile

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎯 AI Match Score | Estimates resume-job compatibility |
| 📊 ATS Score | Evaluates resume content against job requirements |
| 🧠 Semantic Analysis | Uses NLP to compare contextual similarity |
| 🔑 Keyword Analysis | Identifies important job-related keywords |
| 💼 Skill Matching | Highlights matched and missing skills |
| 💪 Strength Analysis | Identifies resume strengths |
| ⚠️ Weakness Analysis | Highlights areas for improvement |
| 💡 AI Recommendations | Provides resume improvement suggestions |
| 🚀 Job Role Suggestions | Suggests potentially relevant career roles |
| 📚 Learning Resources | Helps users explore missing skills |
| 📄 PDF Report | Generates downloadable analysis reports |
| 📱 Responsive Interface | Supports desktop and mobile browsers |
| 🌓 Light / Dark Theme | Offers interface theme options |
| 📑 PDF & DOCX Support | Accepts supported resume formats |

---

## 🧠 How It Works

1. Upload a resume in PDF or DOCX format.
2. Extract and process the resume text.
3. Enter the target job description.
4. Generate text embeddings using Sentence Transformers.
5. Compare resume and job-description embeddings using cosine similarity.
6. Analyze skills, keywords, and potential gaps.
7. Display scores, insights, and recommendations.
8. Generate a downloadable PDF report.

---

## 🔬 AI & NLP Techniques

### 🧠 Semantic Similarity

Sentence Transformers generate embeddings for resume and job-description text. Scikit-learn's `cosine_similarity()` is used to compare the embeddings.

This helps assess contextual similarity instead of relying only on exact keyword matches.

### 🔑 Keyword Matching

Job-related keywords are compared against resume content to identify relevant terms and possible gaps.

### 💼 Skill Matching

The application identifies matched and potentially missing skills to help users understand areas for improvement.

---

## 📊 Analysis Dashboard

The application includes analysis sections for:

- 🎯 AI Match Score
- 🧠 Semantic Analysis
- ✅ Matched Skills
- ❌ Missing Skills
- 📊 ATS Score
- 🔑 Keyword Analysis
- 💪 Strengths and Weaknesses
- 💡 AI Recommendations
- 🚀 Suggested Job Roles
- 📄 PDF Report

---

## 🛠️ Tech Stack

**Programming Language**
- Python

**Application Framework**
- Streamlit

**Machine Learning**
- Scikit-learn
- Sentence Transformers
- Cosine Similarity

**Data Processing**
- NumPy
- Pandas

**Document Processing**
- PyPDF2
- python-docx

**PDF Report Generation**
- ReportLab

---

## 📁 Project Structure

```text
ai-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/anushka23x/ai-Resume-Analyzer.git
```

### 2. Navigate to the Project

```bash
cd ai-Resume-Analyzer
```

### 3. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open locally in your browser.

---

## 📋 Supported Resume Formats

- 📄 PDF
- 📝 DOCX

---

## 🎯 Who Can Use This?

- College students
- Freshers
- Software developers
- Job seekers
- Career switchers
- Placement candidates
- Candidates optimizing their resumes for specific roles

---

## 🚀 Future Enhancements

Potential future improvements include:

- 🔐 User authentication
- 👤 User profiles
- ☁️ Cloud database integration
- 🤖 Generative AI resume suggestions
- 📄 AI Resume Builder
- 🎤 AI Interview Preparation
- 💬 AI Career Assistant
- 📊 Advanced Analytics Dashboard
- 📌 Resume Version Tracking
- 🌍 Multilingual Resume Analysis

---

## 🧪 Project Status

**Status:** Core application deployed; ongoing improvements may be added.

The application provides resume analysis, skill matching, semantic similarity, recommendations, and PDF reporting features.

---

## 👩‍💻 Author

### Anushka

GitHub account and project repository:

- **GitHub Profile:** [github.com/anushka23x](https://github.com/anushka23x)
- **Project Repository:** [AI Resume Analyzer](https://github.com/anushka23x/ai-Resume-Analyzer)
- **Live Application:** [Try the App](https://ai-resume-analyzer-en7y4od9e9owns7usjqtnu.streamlit.app/)

---

## ⭐ Show Your Support

If you find this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest improvements

---

## 📜 License

This project is developed for educational and project-development purposes.

---

<p align="center">

### 🤖 AI Resume Analyzer

**Built with Python • Streamlit • NLP • Machine Learning**

</p>
