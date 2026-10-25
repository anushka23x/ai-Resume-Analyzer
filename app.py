import re
from io import BytesIO
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

import PyPDF2
from docx import Document

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🌓 THEME SELECTOR
# ============================================================

theme = st.sidebar.radio(
    "🎨 Choose Theme",
    ["☀️ White", "🌙 Dark"],
    index=0
)


# ============================================================
# ☀️ WHITE THEME
# ============================================================

if theme == "☀️ White":

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #ffffff;
            color: #222222;
        }

        [data-testid="stSidebar"] {
            background-color: #f5f7fa;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 🌙 DARK THEME
# ============================================================

else:

    st.markdown(
        """
        <style>

        /* Main App */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161b22;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Headings */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: #ffffff !important;
        }

        /* Normal Text */
        p,
        span,
        label {
            color: #ffffff;
        }

        /* Text Inputs */
        textarea,
        input {
            background-color: #1e2530 !important;
            color: #ffffff !important;
        }

        /* Select Box */
        [data-baseweb="select"] > div {
            background-color: #1e2530;
            color: #ffffff;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background-color: #1e2530;
            border-radius: 12px;
            padding: 15px;
        }

        /* Buttons */
        .stButton button,
        .stDownloadButton button,
        .stLinkButton a {
            border-radius: 10px;
        }

        /* Divider */
        hr {
            border-color: #444444;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ⬇️ REST OF YOUR RESUME ANALYZER CODE STARTS HERE
# ============================================================


# 2️⃣ Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 3️⃣ YAHAN authentication code lagega

# 🔐 Authentication code
# jo maine pichhle message mein diya tha


# 4️⃣ Authentication ke baad
# tumhara existing Resume Analyzer code
# continue hoga

# ============================================================
# 🔐 USER AUTHENTICATION
# ============================================================

USERS_FILE = Path("users.json")


def load_users():
    if not USERS_FILE.exists():
        return {}

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def signup_user(username, password):
    users = load_users()

    if username in users:
        return False, "Username already exists."

    users[username] = {
        "password": hash_password(password)
    }

    save_users(users)

    return True, "Account created successfully!"


def login_user(username, password):
    users = load_users()

    if username not in users:
        return False

    return users[username]["password"] == hash_password(password)


# ============================================================
# 🔐 LOGIN / SIGNUP SCREEN
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:40px 0 20px 0;
        ">
            <h1>🤖 AI Resume Analyzer</h1>
            <p style="font-size:18px;">
                AI-powered Resume & Job Description Matching
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])

    # ========================================================
    # SIGN IN
    # ========================================================

    with tab1:

        st.subheader("🔐 Welcome Back")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🚀 Sign In",
            use_container_width=True
        ):

            if not login_username or not login_password:

                st.warning(
                    "Please enter username and password."
                )

            elif login_user(
                login_username,
                login_password
            ):

                st.session_state.logged_in = True
                st.session_state.username = login_username

                st.success("Login successful! 🎉")

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    # ========================================================
    # SIGN UP
    # ========================================================

    with tab2:

        st.subheader("📝 Create Your Account")

        signup_username = st.text_input(
            "Create Username",
            key="signup_username"
        )

        signup_password = st.text_input(
            "Create Password",
            type="password",
            key="signup_password"
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            if not signup_username or not signup_password:

                st.warning(
                    "Please fill all fields."
                )

            elif signup_password != signup_confirm:

                st.error(
                    "Passwords do not match."
                )

            elif len(signup_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                success, message = signup_user(
                    signup_username,
                    signup_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Now go to the Sign In tab and login."
                    )

                else:

                    st.error(message)

    # Stop the Resume Analyzer until user logs in
    st.stop()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================
       HEADER
       ========================= */

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .subtitle {
        text-align: center;
        font-size: 19px;
        color: #666666;
        margin-bottom: 25px;
    }


    /* =========================
       SECTION TITLE
       ========================= */

    .section-title {
        font-size: 27px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* =========================
       HERO CARD
       ========================= */

    .hero-card {
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #e0e0e0;
        background: linear-gradient(
            135deg,
            #f8fafc,
            #eef2ff
        );
        margin-bottom: 25px;
    }


    /* =========================
       SCORE CARDS
       ========================= */

    .score-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        text-align: center;
        min-height: 120px;
    }

    .score-number {
        font-size: 32px;
        font-weight: 800;
    }

    .score-label {
        font-size: 14px;
        color: #64748b;
        margin-top: 5px;
    }


    /* =========================
       SKILL CARDS
       ========================= */

    .skill-match {
        background-color: #ecfdf3;
        border: 1px solid #b7dfc0;
        padding: 11px;
        border-radius: 9px;
        margin-bottom: 8px;
    }

    .skill-missing {
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        padding: 11px;
        border-radius: 9px;
        margin-bottom: 8px;
    }

    .keyword-found {
        background-color: #ecfdf3;
        border: 1px solid #bbf7d0;
        padding: 9px;
        border-radius: 8px;
        margin-bottom: 7px;
    }

    .keyword-missing {
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        padding: 9px;
        border-radius: 8px;
        margin-bottom: 7px;
    }


    /* =========================
       INFORMATION BOX
       ========================= */

    .info-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 17px;
        border-radius: 11px;
        margin-bottom: 15px;
        line-height: 1.6;
    }


    /* =========================
       STRENGTH / WEAKNESS
       ========================= */

    .strength-box {
        background-color: #ecfdf3;
        border: 1px solid #bbf7d0;
        padding: 15px;
        border-radius: 11px;
        margin-bottom: 10px;
        line-height: 1.5;
    }

    .weakness-box {
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        padding: 15px;
        border-radius: 11px;
        margin-bottom: 10px;
        line-height: 1.5;
    }


    /* =========================
       RECOMMENDATION
       ========================= */

    .recommendation-box {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        padding: 15px;
        border-radius: 11px;
        margin-bottom: 10px;
        line-height: 1.5;
    }


    /* =========================
       ROLE CARD
       ========================= */

    .role-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 10px;
    }


    /* =========================
       REPORT BOX
       ========================= */

    .report-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 22px;
        border-radius: 13px;
        margin-top: 15px;
    }


    /* =========================
       STATUS
       ========================= */

    .status-card {
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }


    /* =========================
       MOBILE
       ========================= */

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

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 AI Resume Analyzer")

    st.write(
        "Analyze your resume against any job description "
        "using NLP and machine learning."
    )

    st.divider()

    st.markdown("### ✨ Features")

    st.write("🎯 AI Match Score")
    st.write("📊 ATS Score")
    st.write("🧠 Semantic Analysis")
    st.write("💼 Skill Matching")
    st.write("🔎 Keyword Analysis")
    st.write("💪 Strengths & Weaknesses")
    st.write("💡 AI Recommendations")
    st.write("🚀 Job Role Suggestions")
    st.write("📄 PDF Report")

    st.divider()

    st.caption(
        "Built with Python • Streamlit • NLP • "
        "Machine Learning"
    )


# ============================================================
# AI MODEL
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

    try:

        uploaded_file.seek(0)

        reader = PyPDF2.PdfReader(
            uploaded_file
        )

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        return text

    except Exception as error:

        st.error(
            f"❌ Error reading PDF: {error}"
        )

        return ""


# ============================================================
# DOCX TEXT EXTRACTION
# ============================================================

def extract_docx_text(uploaded_file):

    try:

        uploaded_file.seek(0)

        document = Document(
            uploaded_file
        )

        text = ""

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text += paragraph.text + "\n"

        return text

    except Exception as error:

        st.error(
            f"❌ Error reading DOCX: {error}"
        )

        return ""


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

    text = text.replace(
        "•",
        " "
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
        "artificial-intelligence",
        "ai"
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

    "C": [
        " c ",
        "c programming",
        "c language"
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
        "react.js",
        "reactjs"
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

    "Cybersecurity": [
        "cybersecurity",
        "cyber security"
    ],

    "Linux": [
        "linux"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],

    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Power BI": [
        "power bi"
    ],

    "Tableau": [
        "tableau"
    ],

    "Figma": [
        "figma"
    ],

    "Arduino": [
        "arduino"
    ],

    "IoT": [
        "iot",
        "internet of things"
    ]
}


# ============================================================
# SKILL DETECTION
# ============================================================

def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            alias_clean = alias.strip().lower()

            pattern = (
                r"(?<!\w)"
                +
                re.escape(alias_clean)
                +
                r"(?!\w)"
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
# 🎥 LEARNING / VIDEO SUGGESTIONS
# ============================================================

def get_learning_suggestions(missing_skills):

    suggestions = {

        "JavaScript": {
            "title": "JavaScript for Beginners",
            "description": "Learn JavaScript fundamentals, functions, arrays, DOM and ES6.",
            "search": "JavaScript beginners full course"
        },

        "React": {
            "title": "React JS Complete Guide",
            "description": "Learn React components, props, state, hooks and modern React development.",
            "search": "React JS complete course beginners"
        },

        "Python": {
            "title": "Python Programming",
            "description": "Improve Python programming, functions, OOP and problem solving.",
            "search": "Python programming full course"
        },

        "SQL": {
            "title": "SQL & Database Fundamentals",
            "description": "Learn SQL queries, joins, filtering, grouping and database concepts.",
            "search": "SQL full course beginners"
        },

        "Artificial Intelligence": {
            "title": "Artificial Intelligence Fundamentals",
            "description": "Learn AI concepts, intelligent systems and practical AI applications.",
            "search": "Artificial Intelligence beginners course"
        },

        "Machine Learning": {
            "title": "Machine Learning Fundamentals",
            "description": "Learn regression, classification, supervised learning and model evaluation.",
            "search": "Machine Learning beginners full course"
        },

        "Git": {
            "title": "Git & GitHub",
            "description": "Learn repositories, commits, branches, merging and GitHub workflows.",
            "search": "Git GitHub complete course beginners"
        },

        "C++": {
            "title": "C++ Programming",
            "description": "Improve C++ fundamentals, OOP, STL and problem solving.",
            "search": "C++ complete course beginners"
        },

        "Java": {
            "title": "Java Programming",
            "description": "Learn Java fundamentals, OOP, collections and exception handling.",
            "search": "Java complete course beginners"
        },

        "HTML": {
            "title": "HTML Web Development",
            "description": "Learn semantic HTML, forms and modern webpage structure.",
            "search": "HTML complete course beginners"
        },

        "CSS": {
            "title": "CSS Web Design",
            "description": "Learn Flexbox, Grid, responsive design and modern CSS.",
            "search": "CSS complete course beginners"
        },

        "Data Structures": {
            "title": "Data Structures & Algorithms",
            "description": "Improve arrays, linked lists, stacks, queues, trees and algorithms.",
            "search": "Data Structures Algorithms beginners course"
        }
    }

    results = []

    for skill in missing_skills:

        if skill in suggestions:
            results.append(suggestions[skill])

    return results

# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(
    text,
    section_names
):

    if not text:

        return ""

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    heading_pattern = (
        r"(?im)^[ \t]*("
        +
        "|".join(
            re.escape(section)
            for section in section_names
        )
        +
        r")[ \t]*:?[ \t]*$"
    )

    match = re.search(
        heading_pattern,
        text
    )

    if not match:

        return ""

    start_position = match.end()

    all_sections = [
        "education",
        "academic background",
        "educational qualification",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "certifications",
        "certificates",
        "certification",
        "skills",
        "technical skills",
        "technical expertise",
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
        +
        "|".join(
            re.escape(section)
            for section in all_sections
        )
        +
        r")[ \t]*:?[ \t]*$"
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
# EDUCATION
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
# EXPERIENCE
# ============================================================

def extract_experience(text):

    return extract_section(
        text,
        [
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "internship",
            "internships"
        ]
    )


# ============================================================
# PROJECTS
# ============================================================

def extract_projects(text):

    return extract_section(
        text,
        [
            "projects",
            "project",
            "academic projects",
            "personal projects"
        ]
    )


# ============================================================
# CERTIFICATIONS
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
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🤖 AI Resume Analyzer
    </div>

    <div class="subtitle">
        AI-powered Resume & Job Description Matching
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()
# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    reader = PyPDF2.PdfReader(uploaded_file)

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

    document = Document(uploaded_file)

    text = ""

    # Paragraphs
    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    # Tables
    for table in document.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                if cell.text.strip():

                    row_text.append(
                        cell.text.strip()
                    )

            if row_text:

                text += " | ".join(row_text) + "\n"

    return text


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_resume_text(uploaded_file):

    if uploaded_file is None:

        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):

        return extract_pdf_text(uploaded_file)

    elif filename.endswith(".docx"):

        return extract_docx_text(uploaded_file)

    return ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    if not text:

        return ""

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("•", " ")
    text = text.replace("|", " ")

    # Fix common PDF extraction problems
    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

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

            if re.search(pattern, text):

                found_skills.append(
                    canonical_skill
                )

                break

    return sorted(
        list(set(found_skills))
    )


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(text, section_names):

    if not text:

        return ""

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    heading_pattern = (
        r"(?im)^[ \t]*(?:"
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
            + next_match.start()
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
# EDUCATION
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
# EXPERIENCE
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
# PROJECTS
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
# CERTIFICATIONS
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
            min(score, 100)
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
            matched.intersection(required)
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
    # JOB KEYWORDS
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
    # SKILL SCORE
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
    # SECTION SCORE
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
    # CONTACT SCORE
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
# FINAL MATCH SCORE
# ============================================================

def calculate_final_score(
    semantic_score,
    skill_score
):

    final_score = (

        semantic_score * 0.70

        + skill_score * 0.30

    )

    return round(
        max(
            0,
            min(
                final_score,
                100
            )
        ),
        2
    )


# ============================================================
# MATCH LEVEL
# ============================================================

def get_match_level(score):

    if score >= 80:

        return (
            "Excellent Match",
            "🟢",
            "Your resume strongly matches this role."
        )

    elif score >= 60:

        return (
            "Good Match",
            "🟡",
            "Your resume matches the role but can still be improved."
        )

    elif score >= 40:

        return (
            "Moderate Match",
            "🟠",
            "Consider adding relevant skills and experience."
        )

    else:

        return (
            "Low Match",
            "🔴",
            "Your resume needs significant improvement for this role."
        )


# ============================================================
# EMAIL EXTRACTION
# ============================================================

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:

        return match.group(0)

    return "Not detected"


# ============================================================
# PHONE EXTRACTION
# ============================================================

def extract_phone(text):

    matches = re.findall(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if matches:

        return matches[0]

    return "Not detected"


# ============================================================
# WORD COUNT
# ============================================================

def get_word_count(text):

    if not text:

        return 0

    return len(
        re.findall(
            r"\b\w+\b",
            text
        )
    )


# ============================================================
# RESUME QUALITY SCORE
# ============================================================

def calculate_resume_quality(
    resume_text,
    education,
    experience,
    projects,
    certifications,
    resume_skills
):

    score = 0

    if len(resume_text) > 500:
        score += 20

    if education:
        score += 20

    if experience:
        score += 20

    if projects:
        score += 20

    if certifications:
        score += 10

    if len(resume_skills) >= 5:
        score += 10

    return min(score, 100)
# ============================================================
# AI RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    final_score,
    semantic_score,
    ats_score,
    matched_skills,
    missing_skills,
    resume_skills,
    projects,
    experience
):

    recommendations = []

    # Missing skills
    if missing_skills:

        recommendations.append(
            "Add these missing skills to your resume only if "
            "you genuinely have experience with them: "
            + ", ".join(missing_skills)
            + "."
        )

    else:

        recommendations.append(
            "Your resume covers the major skills detected "
            "in this job description."
        )

    # Match score
    if final_score < 40:

        recommendations.append(
            "The overall match is low. Customize your resume "
            "more closely according to the target job description."
        )

    elif final_score < 60:

        recommendations.append(
            "Improve alignment between your resume and the "
            "target job description."
        )

    elif final_score < 80:

        recommendations.append(
            "Your resume has a good foundation. Add more "
            "role-specific keywords and measurable achievements."
        )

    else:

        recommendations.append(
            "Your resume is strongly aligned with this role. "
            "Focus on measurable achievements and impact."
        )

    # Semantic score
    if semantic_score < 50:

        recommendations.append(
            "Your resume content has low semantic similarity "
            "with the job description. Rewrite relevant experience "
            "and project descriptions using terminology from the role."
        )

    # ATS
    if ats_score < 70:

        recommendations.append(
            "Improve ATS compatibility by using clear headings, "
            "standard terminology, relevant keywords, and concise bullet points."
        )

    # Projects
    if projects:

        recommendations.append(
            "Highlight your strongest projects using the format: "
            "Problem → Technology → Solution → Result."
        )

    else:

        recommendations.append(
            "Add relevant technical projects that demonstrate "
            "the skills required by the target role."
        )

    # Experience
    if experience:

        recommendations.append(
            "Add measurable results to your experience bullets "
            "where possible, such as percentages, users, time saved, "
            "or project outcomes."
        )

    else:

        recommendations.append(
            "Consider adding internships, freelance work, "
            "open-source contributions, or relevant practical experience."
        )

    # General
    recommendations.append(
        "Keep your resume concise, use clear section headings, "
        "and avoid unnecessary information."
    )

    recommendations.append(
        "Never add a skill to your resume unless you actually "
        "know or have experience with it."
    )

    return recommendations


# ============================================================
# STRENGTHS
# ============================================================

def generate_strengths(
    resume_skills,
    matched_skills,
    education,
    experience,
    projects,
    certifications,
    ats_score
):

    strengths = []

    if len(matched_skills) >= 5:

        strengths.append(
            f"Strong technical skill alignment with "
            f"{len(matched_skills)} matched skills."
        )

    elif len(matched_skills) > 0:

        strengths.append(
            f"Resume contains {len(matched_skills)} "
            f"skills relevant to the target role."
        )

    if education:

        strengths.append(
            "Education details are clearly detected in the resume."
        )

    if experience:

        strengths.append(
            "Professional or internship experience is present."
        )

    if projects:

        strengths.append(
            "Technical projects are included in the resume."
        )

    if certifications:

        strengths.append(
            "Certifications and achievements are present."
        )

    if (
        "Git" in resume_skills
        or
        "GitHub" in resume_skills
    ):

        strengths.append(
            "Version control experience with Git/GitHub is present."
        )

    if "Problem Solving" in resume_skills:

        strengths.append(
            "Problem-solving ability is highlighted."
        )

    if ats_score >= 70:

        strengths.append(
            "Good ATS keyword and resume structure alignment."
        )

    return strengths


# ============================================================
# WEAKNESSES
# ============================================================

def generate_weaknesses(
    missing_skills,
    semantic_score,
    skill_score,
    ats_score,
    experience,
    projects
):

    weaknesses = []

    if missing_skills:

        weaknesses.append(
            "Missing job-specific skills: "
            + ", ".join(missing_skills)
            + "."
        )

    if semantic_score < 50:

        weaknesses.append(
            "Low semantic similarity with the target job description."
        )

    elif semantic_score < 70:

        weaknesses.append(
            "Semantic alignment with the target role can be improved."
        )

    if skill_score < 60:

        weaknesses.append(
            "Technical skill coverage can be improved for this role."
        )

    if ats_score < 70:

        weaknesses.append(
            "ATS keyword alignment can be improved."
        )

    if not experience:

        weaknesses.append(
            "No professional experience section was detected."
        )

    if not projects:

        weaknesses.append(
            "No technical projects were detected."
        )

    return weaknesses


# ============================================================
# PDF REPORT GENERATOR
# ============================================================

def generate_pdf_report(
    resume_name,
    semantic_score,
    ats_score,
    final_score,
    resume_skills,
    job_skills,
    matched_skills,
    missing_skills,
    education,
    experience,
    projects,
    certifications,
    recommendations,
    strengths,
    weaknesses
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER
    title_style.fontSize = 22

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            f"<b>Resume:</b> {resume_name}",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # SCORE
    # ========================================================

    story.append(
        Paragraph(
            "Resume Match Scores",
            heading_style
        )
    )

    score_data = [
        ["Score", "Result"],
        ["Final Match Score", f"{final_score}%"],
        ["AI Semantic Score", f"{semantic_score}%"],
        ["ATS Score", f"{ats_score}%"],
        ["Matched Skills", str(len(matched_skills))]
    ]

    score_table = Table(
        score_data,
        colWidths=[250, 150]
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4e78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ]
        )
    )

    story.append(score_table)

    story.append(
        Spacer(1, 20)
    )

    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    story.append(
        Paragraph(
            "Matched Skills",
            heading_style
        )
    )

    if matched_skills:

        for skill in matched_skills:

            story.append(
                Paragraph(
                    f"✓ {skill}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No matched skills detected.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # MISSING SKILLS
    # ========================================================

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    if missing_skills:

        for skill in missing_skills:

            story.append(
                Paragraph(
                    f"✗ {skill}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No important missing skills detected.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # RESUME SKILLS
    # ========================================================

    story.append(
        Paragraph(
            "Resume Skills",
            heading_style
        )
    )

    story.append(
        Paragraph(
            ", ".join(resume_skills)
            if resume_skills
            else "No skills detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # JOB SKILLS
    # ========================================================

    story.append(
        Paragraph(
            "Job Required Skills",
            heading_style
        )
    )

    story.append(
        Paragraph(
            ", ".join(job_skills)
            if job_skills
            else "No skills detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ========================================================
    # STRENGTHS
    # ========================================================

    story.append(
        Paragraph(
            "Resume Strengths",
            heading_style
        )
    )

    if strengths:

        for strength in strengths:

            story.append(
                Paragraph(
                    f"✓ {strength}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                "No major strengths detected.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # WEAKNESSES
    # ========================================================

    story.append(
        Paragraph(
            "Resume Weaknesses",
            heading_style
        )
    )

    if weaknesses:

        for weakness in weaknesses:

            story.append(
                Paragraph(
                    f"⚠ {weakness}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                "No major weaknesses detected.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 20)
    )

    # ========================================================
    # EDUCATION
    # ========================================================

    story.append(
        Paragraph(
            "Education",
            heading_style
        )
    )

    story.append(
        Paragraph(
            education.replace("\n", "<br/>")
            if education
            else "Education information not detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # EXPERIENCE
    # ========================================================

    story.append(
        Paragraph(
            "Experience",
            heading_style
        )
    )

    story.append(
        Paragraph(
            experience.replace("\n", "<br/>")
            if experience
            else "Experience information not detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # PROJECTS
    # ========================================================

    story.append(
        Paragraph(
            "Projects",
            heading_style
        )
    )

    story.append(
        Paragraph(
            projects.replace("\n", "<br/>")
            if projects
            else "Projects information not detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # CERTIFICATIONS
    # ========================================================

    story.append(
        Paragraph(
            "Certifications",
            heading_style
        )
    )

    story.append(
        Paragraph(
            certifications.replace("\n", "<br/>")
            if certifications
            else "Certification information not detected.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    story.append(
        Paragraph(
            "AI Recommendations",
            heading_style
        )
    )

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        story.append(
            Paragraph(
                f"{index}. {recommendation}",
                normal_style
            )
        )

        story.append(
            Spacer(1, 5)
        )

    story.append(
        Spacer(1, 20)
    )

    # ========================================================
    # FOOTER
    # ========================================================

    story.append(
        Paragraph(
            "Generated by AI Resume Analyzer | "
            "Python • Streamlit • NLP • Machine Learning",
            normal_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


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

        file_size_kb = (
            resume_file.size / 1024
        )

        st.caption(
            f"File size: {file_size_kb:.1f} KB"
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

    job_description = (
        st.session_state.job_description
    )


# ============================================================
# INPUT STATUS
# ============================================================

st.divider()

st.subheader(
    "📋 Input Status"
)

status_col1, status_col2 = st.columns(2)


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

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # EXTRACT RESUME
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # EXTRACT INFORMATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------------

    email = extract_email(
        resume_text
    )

    phone = extract_phone(
        resume_text
    )

    word_count = get_word_count(
        resume_text
    )


    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    with st.spinner(
        "🤖 AI is analyzing your resume..."
    ):

        semantic_score = (
            calculate_semantic_similarity(
                resume_text,
                job_description
            )
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

        ats_score = calculate_ats_score(
            resume_text,
            job_description
        )

        final_score = calculate_final_score(
            semantic_score,
            skill_score
        )


    # --------------------------------------------------------
    # QUALITY SCORE
    # --------------------------------------------------------

    resume_quality = calculate_resume_quality(
        resume_text,
        education,
        experience,
        projects,
        certifications,
        resume_skills
    )


    # --------------------------------------------------------
    # MATCH LEVEL
    # --------------------------------------------------------

    match_title, match_icon, match_message = (
        get_match_level(
            final_score
        )
    )


    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        final_score,
        semantic_score,
        ats_score,
        matched_skills,
        missing_skills,
        resume_skills,
        projects,
        experience
    )


    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    strengths = generate_strengths(
        resume_skills,
        matched_skills,
        education,
        experience,
        projects,
        certifications,
        ats_score
    )


    # --------------------------------------------------------
    # WEAKNESSES
    # --------------------------------------------------------

    weaknesses = generate_weaknesses(
        missing_skills,
        semantic_score,
        skill_score,
        ats_score,
        experience,
        projects
    )


    st.success(
        "✅ Resume analysis completed successfully!"
    )


    # ========================================================
    # SCORE DASHBOARD
    # ========================================================

    st.divider()

    st.subheader(
        "🎯 AI Resume Match Score"
    )

    score_col1, score_col2, score_col3, score_col4 = (
        st.columns(4)
    )


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


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.write(
        "**Overall Resume Match**"
    )

    st.progress(
        int(final_score)
    )


    # --------------------------------------------------------
    # MATCH MESSAGE
    # --------------------------------------------------------

    if final_score >= 80:

        st.success(
            f"{match_icon} **{match_title}** — "
            f"{match_message}"
        )

    elif final_score >= 60:

        st.info(
            f"{match_icon} **{match_title}** — "
            f"{match_message}"
        )

    elif final_score >= 40:

        st.warning(
            f"{match_icon} **{match_title}** — "
            f"{match_message}"
        )

    else:

        st.error(
            f"{match_icon} **{match_title}** — "
            f"{match_message}"
        )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.markdown(
        "### 📊 Score Breakdown"
    )

    breakdown_col1, breakdown_col2 = st.columns(2)


    with breakdown_col1:

        st.write(
            f"**Semantic Relevance:** "
            f"{semantic_score}%"
        )

        st.progress(
            int(semantic_score)
        )

        st.write(
            f"**Technical Skill Match:** "
            f"{skill_score}%"
        )

        st.progress(
            int(skill_score)
        )


    with breakdown_col2:

        st.write(
            f"**ATS Compatibility:** "
            f"{ats_score}%"
        )

        st.progress(
            int(ats_score)
        )

        st.write(
            f"**Resume Quality:** "
            f"{resume_quality}%"
        )

        st.progress(
            int(resume_quality)
        )


    # ========================================================
    # RESUME OVERVIEW
    # ========================================================

    st.divider()

    st.subheader(
        "📌 Resume Overview"
    )

    overview_col1, overview_col2, overview_col3, overview_col4 = (
        st.columns(4)
    )


    with overview_col1:

        st.metric(
            "Resume Words",
            word_count
        )


    with overview_col2:

        st.metric(
            "Detected Skills",
            len(resume_skills)
        )


    with overview_col3:

        st.metric(
            "Job Skills",
            len(job_skills)
        )


    with overview_col4:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )


    # ========================================================
    # CONTACT INFORMATION
    # ========================================================

    with st.expander(
        "👤 Detected Contact Information"
    ):

        contact_col1, contact_col2 = st.columns(2)

        with contact_col1:

            st.write(
                f"**Email:** {email}"
            )

        with contact_col2:

            st.write(
                f"**Phone:** {phone}"
            )


    # ========================================================
    # EXTRACTED RESUME INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "📌 Extracted Resume Information"
    )

    info_col1, info_col2 = st.columns(2)


    # --------------------------------------------------------
    # EDUCATION + EXPERIENCE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # PROJECTS + CERTIFICATIONS
    # --------------------------------------------------------

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

    skill_col1, skill_col2 = st.columns(2)


    # --------------------------------------------------------
    # MATCHED
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # MISSING
    # --------------------------------------------------------

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

    detected_col1, detected_col2 = st.columns(2)


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
# ============================================================
# 📺 LEARNING VIDEOS FOR MISSING SKILLS
# ============================================================

st.subheader("📚 Learn Missing Skills")

if missing_skills:

    for skill in missing_skills:

        st.markdown(f"### 🎯 {skill}")

        # YouTube search URL
        skill_query = skill.replace(" ", "+")
        youtube_url = (
            f"https://www.youtube.com/results?search_query="
            f"{skill_query}+tutorial+for+beginners"
        )

        # Video learning button
        st.link_button(
            f"▶️ Learn {skill} — Watch Lecture",
            youtube_url,
            use_container_width=True
        )

        st.caption(
            f"📚 Recommended: Learn {skill} from beginner "
            f"to advanced level."
        )

        st.divider()

else:

    st.success(
        "🎉 No major missing skills detected! "
        "Your resume covers the required skills."
    )
 # ============================================================
# 📄 PDF REPORT DOWNLOAD
# ============================================================

st.divider()

st.subheader("📄 Download Resume Analysis Report")

pdf_buffer = BytesIO()

doc = SimpleDocTemplate(
    pdf_buffer,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

story = []

story.append(
    Paragraph(
        "AI Resume Analyzer Report",
        styles["Title"]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        f"<b>Resume:</b> {resume_file.name}",
        styles["BodyText"]
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        f"<b>Final Match Score:</b> {final_score:.2f}%",
        styles["BodyText"]
    )
)

story.append(
    Paragraph(
        f"<b>AI Semantic Score:</b> {semantic_score:.2f}%",
        styles["BodyText"]
    )
)

story.append(
    Paragraph(
        f"<b>ATS Score:</b> {ats_score:.2f}%",
        styles["BodyText"]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        "Matched Skills",
        styles["Heading2"]
    )
)

story.append(
    Paragraph(
        ", ".join(matched_skills) if matched_skills else "None",
        styles["BodyText"]
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "Missing Skills",
        styles["Heading2"]
    )
)

story.append(
    Paragraph(
        ", ".join(missing_skills) if missing_skills else "None",
        styles["BodyText"]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        "AI Recommendations",
        styles["Heading2"]
    )
)

if recommendations:
    for i, recommendation in enumerate(recommendations, 1):
        story.append(
            Paragraph(
                f"{i}. {recommendation}",
                styles["BodyText"]
            )
        )
        story.append(Spacer(1, 5))
else:
    story.append(
        Paragraph(
            "No recommendations available.",
            styles["BodyText"]
        )
    )

doc.build(story)

pdf_buffer.seek(0)

st.download_button(
    label="📥 Download AI Resume Report (PDF)",
    data=pdf_buffer.getvalue(),
    file_name="AI_Resume_Analysis_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)