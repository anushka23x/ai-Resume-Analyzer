import re

import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import PyPDF2
from docx import Document


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .skill-match {
        background-color: #eaf7ed;
        border: 1px solid #b7dfc0;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    .skill-missing {
        background-color: #fdecec;
        border: 1px solid #f0b5b5;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    .info-box {
        background-color: #f5f7fa;
        border: 1px solid #dfe3e8;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .hero-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #f5f7fa;
        border: 1px solid #e0e0e0;
        margin-bottom: 25px;
    }

    @media (max-width: 700px) {

        .main-title {
            font-size: 34px;
        }

        .subtitle {
            font-size: 15px;
        }

        .section-title {
            font-size: 23px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD AI MODEL
# ============================================================

@st.cache_resource
def load_ai_model():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    reader = PyPDF2.PdfReader(
        uploaded_file
    )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ============================================================
# DOCX TEXT EXTRACTION
# ============================================================

def extract_docx_text(uploaded_file):

    document = Document(
        uploaded_file
    )

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    return text


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_resume_text(uploaded_file):

    if uploaded_file is None:

        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):

        return extract_pdf_text(
            uploaded_file
        )

    if filename.endswith(".docx"):

        return extract_docx_text(
            uploaded_file
        )

    return ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    if not text:

        return ""

    text = text.lower()

    text = text.replace(
        "–",
        "-"
    )

    text = text.replace(
        "—",
        "-"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_ALIASES = {

    "Artificial Intelligence": [
        "artificial intelligence",
        "artificial-intelligence"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "Natural Language Processing": [
        "natural language processing",
        "natural-language processing",
        "nlp"
    ],

    "Computer Vision": [
        "computer vision",
        "computer-vision"
    ],

    "Generative AI": [
        "generative ai",
        "generative-ai",
        "gen ai"
    ],

    "Large Language Models": [
        "large language models",
        "large language model",
        "llm",
        "llms"
    ],

    "FastAPI": [
        "fastapi",
        "fast api"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes"
    ],

    "TensorFlow": [
        "tensorflow",
        "tensor flow"
    ],

    "PyTorch": [
        "pytorch",
        "py torch"
    ],

    "Scikit-Learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "NumPy": [
        "numpy",
        "num py"
    ],

    "Pandas": [
        "pandas"
    ],

    "REST API": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    ],

    "SQL": [
        "sql",
        "structured query language"
    ],

    "MySQL": [
        "mysql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "Python": [
        "python"
    ],

    "Java": [
        "java"
    ],

    "C++": [
        "c++",
        "cpp"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "TypeScript": [
        "typescript",
        "type script"
    ],

    "HTML": [
        "html"
    ],

    "CSS": [
        "css"
    ],

    "React": [
        "react",
        "react.js"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github",
        "git hub"
    ],

    "Data Structures": [
        "data structures",
        "data structure"
    ],

    "Algorithms": [
        "algorithms",
        "algorithm"
    ],

    "Object Oriented Programming": [
        "object oriented programming",
        "object-oriented programming",
        "oop"
    ],

    "Operating Systems": [
        "operating systems",
        "operating system"
    ],

    "Computer Networks": [
        "computer networks",
        "computer network"
    ],

    "Database Management": [
        "database management",
        "dbms"
    ],

    "Communication": [
        "communication skills",
        "communication"
    ],

    "Leadership": [
        "leadership"
    ],

    "Teamwork": [
        "teamwork",
        "team work"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],
}


# ============================================================
# SKILL DETECTION
# ============================================================

def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias.lower())
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text
            ):

                found_skills.append(
                    canonical_skill
                )

                break

    return sorted(
        list(
            set(found_skills)
        )
    )


# ============================================================
# RESUME SECTION EXTRACTION
# ============================================================

def extract_section(
    text,
    section_names
):

    if not text:

        return ""

    # Convert different line endings
    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    # Section headings
    heading_pattern = (
        r"(?im)^[ \t]*("
        + "|".join(
            re.escape(section)
            for section in section_names
        )
        + r")[ \t]*:?[ \t]*$"
    )

    match = re.search(
        heading_pattern,
        text
    )

    if not match:

        return ""

    start_position = match.end()

    # Common resume section headings
    all_sections = [
        "education",
        "academic background",
        "educational qualification",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "projects",
        "project",
        "academic projects",
        "certifications",
        "certificates",
        "certification",
        "skills",
        "technical skills",
        "achievements",
        "awards",
        "summary",
        "objective",
        "profile",
        "contact",
        "personal details",
        "languages",
        "interests",
        "hobbies"
    ]

    next_heading_pattern = (
        r"(?im)^[ \t]*(?:"
        + "|".join(
            re.escape(section)
            for section in all_sections
        )
        + r")[ \t]*:?[ \t]*$"
    )

    next_match = re.search(
        next_heading_pattern,
        text[start_position:]
    )

    if next_match:

        end_position = (
            start_position
            +
            next_match.start()
        )

        section_text = text[
            start_position:end_position
        ]

    else:

        section_text = text[
            start_position:
        ]

    return section_text.strip()


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

def extract_education(text):

    return extract_section(
        text,
        [
            "education",
            "academic background",
            "educational qualification"
        ]
    )


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text):

    return extract_section(
        text,
        [
            "experience",
            "work experience",
            "professional experience",
            "employment"
        ]
    )


# ============================================================
# PROJECT EXTRACTION
# ============================================================

def extract_projects(text):

    return extract_section(
        text,
        [
            "projects",
            "project",
            "academic projects"
        ]
    )


# ============================================================
# CERTIFICATION EXTRACTION
# ============================================================

def extract_certifications(text):

    return extract_section(
        text,
        [
            "certifications",
            "certificates",
            "certification"
        ]
    )


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    resume_text,
    job_description
):

    if not resume_text.strip():

        return 0.0

    if not job_description.strip():

        return 0.0

    model = load_ai_model()

    embeddings = model.encode(
        [
            resume_text,
            job_description
        ],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = float(similarity) * 100

    return round(
        max(
            0,
            min(
                score,
                100
            )
        ),
        2
    )


# ============================================================
# SKILL SCORE
# ============================================================

def calculate_skill_score(
    matched_skills,
    required_skills
):

    if not required_skills:

        return 0.0

    matched = {
        skill.lower()
        for skill in matched_skills
    }

    required = {
        skill.lower()
        for skill in required_skills
    }

    score = (
        len(
            matched.intersection(
                required
            )
        )
        /
        len(required)
    ) * 100

    return round(
        score,
        2
    )


# ============================================================
# ATS SCORE
# ============================================================

def calculate_ats_score(
    resume_text,
    job_description
):

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    if not resume or not job:

        return 0.0

    # --------------------------------------------------------
    # 1. KEYWORD SCORE
    # --------------------------------------------------------

    job_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job
        )
    )

    resume_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            resume
        )
    )

    if job_words:

        keyword_matches = len(
            job_words.intersection(
                resume_words
            )
        )

        keyword_score = (
            keyword_matches
            /
            len(job_words)
        ) * 100

    else:

        keyword_score = 0


    # --------------------------------------------------------
    # 2. SKILL SCORE
    # --------------------------------------------------------

    resume_skills = set(
        extract_skills(
            resume_text
        )
    )

    job_skills = set(
        extract_skills(
            job_description
        )
    )

    if job_skills:

        matched_skills = len(
            resume_skills.intersection(
                job_skills
            )
        )

        skill_score = (
            matched_skills
            /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0


    # --------------------------------------------------------
    # 3. RESUME SECTION SCORE
    # --------------------------------------------------------

    important_sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certifications"
    ]

    section_count = 0

    for section in important_sections:

        if section in resume:

            section_count += 1

    section_score = (
        section_count
        /
        len(important_sections)
    ) * 100


    # --------------------------------------------------------
    # 4. CONTACT INFORMATION SCORE
    # --------------------------------------------------------

    contact_score = 0

    if re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        resume
    ):

        contact_score += 50

    if re.search(
        r"\+?\d[\d\s().-]{8,}",
        resume
    ):

        contact_score += 50


    # --------------------------------------------------------
    # FINAL ATS SCORE
    # --------------------------------------------------------

    ats_score = (
        keyword_score * 0.30
        + skill_score * 0.40
        + section_score * 0.20
        + contact_score * 0.10
    )

    return round(
        max(
            0,
            min(
                ats_score,
                100
            )
        ),
        2
    )


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(
    semantic_score,
    skill_score
):

    final_score = (
        semantic_score * 0.70
        +
        skill_score * 0.30
    )

    return round(
        final_score,
        2
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Resume Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered Resume & Job Description Matching'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

left_column, right_column = st.columns(
    2
)


# ============================================================
# RESUME UPLOAD
# ============================================================

with left_column:

    st.markdown(
        '<div class="section-title">'
        '📄 Upload Your Resume'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload your resume in PDF or DOCX format."
    )

    resume_file = st.file_uploader(
        "Choose your resume",
        type=[
            "pdf",
            "docx"
        ],
        label_visibility="collapsed"
    )

    if resume_file is not None:

        st.success(
            "Resume uploaded successfully! ✅"
        )

        st.write(
            f"**File:** {resume_file.name}"
        )


# ============================================================
# JOB DESCRIPTION
# ============================================================

with right_column:

    st.markdown(
        '<div class="section-title">'
        '💼 Job Description'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Paste the job description you want to analyze."
    )

    st.text_area(
        "Job Description",
        height=250,
        placeholder="""Example:

Python Developer

We are looking for a Python Developer
with experience in Python, SQL, Pandas,
NumPy, Machine Learning, Git and REST APIs.

Requirements:
- Python
- SQL
- Machine Learning
- Pandas
- NumPy
- Git
- Problem Solving
""",
        label_visibility="collapsed",
        key="job_description"
    )

    job_description = st.session_state.job_description


# ============================================================
# INPUT STATUS
# ============================================================

st.divider()

st.subheader(
    "📋 Input Status"
)

status_col1, status_col2 = st.columns(
    2
)


with status_col1:

    if resume_file is not None:

        st.success(
            "✅ Resume Ready"
        )

    else:

        st.warning(
            "⚠️ Resume Not Uploaded"
        )


with status_col2:

    if job_description.strip():

        st.success(
            "✅ Job Description Ready"
        )

    else:

        st.warning(
            "⚠️ Job Description Missing"
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🔍 Resume Analysis'
    '</div>',
    unsafe_allow_html=True
)

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True,
    type="primary"
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if resume_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

        st.stop()


    if not job_description.strip():

        st.warning(
            "⚠️ Please enter a job description first."
        )

        st.stop()


    # ========================================================
    # EXTRACT RESUME
    # ========================================================

    with st.spinner(
        "📄 Reading your resume..."
    ):

        resume_text = extract_resume_text(
            resume_file
        )


    if not resume_text.strip():

        st.error(
            "❌ Could not extract text from the resume."
        )

        st.stop()


    # ========================================================
    # EXTRACT RESUME INFORMATION
    # ========================================================

    with st.spinner(
        "🧠 Extracting resume information..."
    ):

        resume_skills = extract_skills(
            resume_text
        )

        education = extract_education(
            resume_text
        )

        experience = extract_experience(
            resume_text
        )

        projects = extract_projects(
            resume_text
        )

        certifications = extract_certifications(
            resume_text
        )


    # ========================================================
    # AI ANALYSIS
    # ========================================================

    with st.spinner(
        "🤖 AI is analyzing your resume..."
    ):

        semantic_score = calculate_semantic_similarity(
            resume_text,
            job_description
        )

        ats_score = calculate_ats_score(
            resume_text,
            job_description
        )

        job_skills = extract_skills(
            job_description
        )

        matched_skills = sorted(
            list(
                set(resume_skills)
                &
                set(job_skills)
            )
        )

        missing_skills = sorted(
            list(
                set(job_skills)
                -
                set(resume_skills)
            )
        )

        skill_score = calculate_skill_score(
            matched_skills,
            job_skills
        )

        final_score = calculate_final_score(
            semantic_score,
            skill_score
        )


    st.success(
        "✅ Resume analysis completed!"
    )


    # ========================================================
    # SCORE
    # ========================================================

    st.subheader(
        "🎯 AI Resume Match Score"
    )

    score_col1, score_col2, score_col3, score_col4 = st.columns(4)


    with score_col1:

        st.metric(
            "Final Match Score",
            f"{final_score}%"
        )


    with score_col2:

        st.metric(
            "AI Semantic Score",
            f"{semantic_score}%"
        )


    with score_col3:

        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )


    with score_col4:

        st.metric(
            "Matched Skills",
            len(matched_skills)
        )


    st.progress(
        int(final_score)
    )


    # ========================================================
    # SCORE MESSAGE
    # ========================================================

    if final_score >= 80:

        st.success(
            "🟢 Excellent Match — Your resume strongly "
            "matches this role."
        )

    elif final_score >= 60:

        st.info(
            "🟡 Good Match — Your resume matches the role "
            "but can still be improved."
        )

    elif final_score >= 40:

        st.warning(
            "🟠 Moderate Match — Consider adding relevant "
            "skills and experience."
        )

    else:

        st.error(
            "🔴 Low Match — Your resume needs significant "
            "improvement for this role."
        )


    # ========================================================
    # EXTRACTED RESUME INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "📌 Extracted Resume Information"
    )

    info_col1, info_col2 = st.columns(
        2
    )


    # ========================================================
    # EDUCATION
    # ========================================================

    with info_col1:

        st.markdown(
            "### 🎓 Education"
        )

        if education:

            st.markdown(
                f"""
                <div class="info-box">
                {education.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Education information not detected."
            )


        # ====================================================
        # EXPERIENCE
        # ====================================================

        st.markdown(
            "### 💼 Experience"
        )

        if experience:

            st.markdown(
                f"""
                <div class="info-box">
                {experience.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Experience information not detected."
            )


    # ========================================================
    # PROJECTS + CERTIFICATIONS
    # ========================================================

    with info_col2:

        st.markdown(
            "### 🚀 Projects"
        )

        if projects:

            st.markdown(
                f"""
                <div class="info-box">
                {projects.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Projects information not detected."
            )


        # ====================================================
        # CERTIFICATIONS
        # ====================================================

        st.markdown(
            "### 🏆 Certifications"
        )

        if certifications:

            st.markdown(
                f"""
                <div class="info-box">
                {certifications.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Certification information not detected."
            )


    # ========================================================
    # SKILL ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "🧠 Skill Analysis"
    )

    skill_col1, skill_col2 = st.columns(
        2
    )


    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    with skill_col1:

        st.markdown(
            "### ✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f"""
                    <div class="skill-match">
                    ✅ <b>{skill}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No matching skills detected."
            )


    # ========================================================
    # MISSING SKILLS
    # ========================================================

    with skill_col2:

        st.markdown(
            "### ❌ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f"""
                    <div class="skill-missing">
                    ❌ <b>{skill}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "🎉 No important missing skills detected!"
            )


    # ========================================================
    # DETECTED SKILLS
    # ========================================================

    st.divider()

    st.subheader(
        "📚 Detected Skills"
    )

    detected_col1, detected_col2 = st.columns(
        2
    )


    with detected_col1:

        st.markdown(
            "### 📄 Resume Skills"
        )

        if resume_skills:

            st.write(
                " • ".join(
                    resume_skills
                )
            )

        else:

            st.write(
                "No skills detected."
            )


    with detected_col2:

        st.markdown(
            "### 💼 Job Required Skills"
        )

        if job_skills:

            st.write(
                " • ".join(
                    job_skills
                )
            )

        else:

            st.write(
                "No skills detected."
            )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "💡 AI Recommendations"
    )

    recommendations = []


    if missing_skills:

        recommendations.append(
            "Add these missing skills to your resume "
            "only if you genuinely have experience with them: "
            +
            ", ".join(
                missing_skills
            )
            +
            "."
        )

    else:

        recommendations.append(
            "Your resume covers the major skills "
            "detected in this job description."
        )


    if final_score < 60:

        recommendations.append(
            "Improve the alignment between your resume "
            "and the target job description."
        )

    elif final_score < 80:

        recommendations.append(
            "Your resume has a good foundation. "
            "Add more role-specific keywords and "
            "relevant project details."
        )

    else:

        recommendations.append(
            "Your resume is strongly aligned with this role. "
            "Focus on measurable achievements."
        )


    recommendations.append(
        "Highlight relevant projects using the format: "
        "Problem → Technology → Solution → Result."
    )


    recommendations.append(
        "Keep your resume concise, use clear section headings, "
        "and avoid unnecessary information."
    )


    recommendations.append(
        "Never add a skill to your resume unless you "
        "actually know or have experience with it."
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.info(
            f"💡 **{index}.** {recommendation}"
        )


    # ========================================================
    # RESUME SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Resume Summary"
    )

    summary_col1, summary_col2 = st.columns(
        2
    )


    with summary_col1:

        st.write(
            f"**Resume:** {resume_file.name}"
        )

        st.write(
            f"**Resume Characters:** "
            f"{len(resume_text):,}"
        )

        st.write(
            f"**Detected Resume Skills:** "
            f"{len(resume_skills)}"
        )

        st.write(
            f"**Matched Skills:** "
            f"{len(matched_skills)}"
        )

        st.write(
            f"**Education Detected:** "
            f"{'Yes' if education else 'No'}"
        )

        st.write(
            f"**Experience Detected:** "
            f"{'Yes' if experience else 'No'}"
        )


    with summary_col2:

        st.write(
            f"**Job Description Characters:** "
            f"{len(job_description):,}"
        )

        st.write(
            f"**Required Skills Detected:** "
            f"{len(job_skills)}"
        )

        st.write(
            f"**Missing Skills:** "
            f"{len(missing_skills)}"
        )

        st.write(
            f"**Projects Detected:** "
            f"{'Yes' if projects else 'No'}"
        )

        st.write(
            f"**Certifications Detected:** "
            f"{'Yes' if certifications else 'No'}"
        )

        st.write(
            f"**ATS Score:** "
            f"{ats_score}%"
        )

        st.write(
            f"**Final AI Match Score:** "
            f"{final_score}%"
        )


    # ========================================================
    # EXTRACTED RESUME TEXT
    # ========================================================

    st.divider()

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Resume text",
            resume_text,
            height=300,
            label_visibility="collapsed"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Resume Analyzer | "
    "Built with Python, Streamlit, NLP & Machine Learning"
)