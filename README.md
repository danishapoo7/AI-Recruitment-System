# 🚀 AI Recruitment System

An **AI-powered recruitment platform** that automates resume screening and candidate ranking using **Natural Language Processing (NLP)** and **Machine Learning**. The system matches resumes against job descriptions, extracts skills, explains AI decisions, and helps recruiters shortlist the best candidates quickly.

---

# 📌 Features

### 🧠 AI Resume Matching

* Matches resumes against job descriptions using:

  * **TF-IDF similarity**
  * **Semantic similarity (Sentence Transformers / BERT)**

### 📊 Candidate Ranking

* Automatically ranks candidates based on similarity score
* Displays results in a structured table

### 🔍 Skill Extraction

* Extracts skills from resumes using NLP
* Detects technical skills such as:

  * Python
  * SQL
  * Cybersecurity
  * Linux
  * Machine Learning

### 🧠 Explainable AI

Shows **why a candidate matched**:

* ✅ Matched Skills
* ❌ Missing Skills

This improves **AI transparency and recruiter trust**.

### 📂 Multiple Resume Upload

Recruiters can upload **multiple resumes simultaneously** and match them against a job description.

### 👩‍💼 Recruiter Dashboard

Provides tools for recruiters to:

* View ranked candidates
* Search candidates by skills
* Approve / Deny candidates
* Schedule interviews

### 📅 Interview Scheduling

Recruiters can schedule interviews directly from the dashboard.

### 🔐 Authentication System

Includes:

* Login system
* Role-based access control
* Admin and recruiter permissions

### 📊 Analytics Dashboard

Provides recruitment insights:

* Candidate skill distribution
* Score distribution
* Total candidates processed

### ⚖️ Ethical AI (Bias Mitigation)

Sensitive information such as:

* Gender
* Religion
* Marital status

is removed during processing to ensure **fair candidate evaluation**.

---

# 🏗️ System Architecture

```
Frontend (Streamlit)
        │
        │ REST API
        ▼
Backend (FastAPI)
        │
        ├── NLP Processing
        ├── Resume Matching Engine
        ├── Explainable AI Module
        ▼
Database (MongoDB)
```

---

# ⚙️ Tech Stack

### Frontend

* **Streamlit**
* Python

### Backend

* **FastAPI**
* Python

### Machine Learning / NLP

* **Scikit-learn**
* **Sentence Transformers**
* **SpaCy**
* **PDFMiner**

### Database

* **MongoDB**

### Authentication

* **JWT Authentication**
* **Passlib / Bcrypt**

---

# 📂 Project Structure

```
ai-recruitment-system
│
├── backend
│   ├── main.py
│   ├── database.py
│   ├── matching.py
│   ├── semantic_matching.py
│   ├── nlp.py
│   ├── explainable.py
│   └── auth.py
│
├── frontend
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/danishapoo7/ai-recruitment-system.git
cd ai-recruitment-system
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

### Start Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Start Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

Frontend runs on:

```
http://localhost:8501
```

---

# 📊 Example Workflow

1️⃣ Recruiter uploads multiple resumes
2️⃣ System extracts resume content
3️⃣ AI compares resumes with job description
4️⃣ Candidates are ranked by similarity score
5️⃣ Recruiter reviews matched and missing skills
6️⃣ Recruiter approves or schedules interviews

---

# 🧠 Explainable AI Example

| Candidate   | Score | Matched Skills | Missing Skills |
| ----------- | ----- | -------------- | -------------- |
| Resume1.pdf | 0.87  | Python, SQL    | Docker         |
| Resume2.pdf | 0.65  | Linux          | Python         |

---

# 🔐 Roles

| Role      | Permissions                   |
| --------- | ----------------------------- |
| Admin     | Full system control           |
| Recruiter | Review and approve candidates |

---

# 📈 Future Improvements

* AI Interview Question Generator
* Resume skill gap analysis
* Automated email notifications
* Resume parsing using LLMs
* Dashboard visualizations
* Cloud deployment (AWS / Docker)

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Muhammed Danish AP**

Cybersecurity & AI Enthusiast

---

# ⭐ If you like this project

Give it a **star ⭐ on GitHub** to support the project.

