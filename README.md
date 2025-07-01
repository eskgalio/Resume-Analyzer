# AI-Powered Resume Analyzer

![Resume Analyzer Banner](https://img.shields.io/badge/AI%20Resume%20Analyzer-Powered%20by%20Python%20%7C%20Flask%20%7C%20spaCy-blue)

A modern, open-source, AI-powered web app that analyzes resumes, provides actionable improvement suggestions, checks ATS compliance, and matches candidates to job roles using NLP and machine learning.

---

## 🚀 Features

- **Upload Resume (PDF/TXT)**: Securely upload and analyze resumes.
- **NLP Analysis**: Extracts skills, education, and experience using spaCy.
- **Improvement Suggestions**: Personalized tips to enhance your resume.
- **Job Role Matching**: Matches your profile to relevant job roles.
- **ATS Compliance Check**: Flags issues that may affect Applicant Tracking Systems.
- **Resume Scoring**: Get a 0-100 score based on best practices.
- **Keyword Gap Analysis**: Compare your resume to a job description and see missing keywords.
- **PDF Report Download**: Download a branded analysis report.
- **Modern Responsive UI**: Works on mobile, tablet, and desktop.
- **Privacy First**: Resumes are deleted after analysis. No data is shared.

---

## 🖥️ Screenshots

![Home Page](screenshots/home.png)
![Analysis Result](screenshots/result.png)

---

## 🛠️ Tech Stack
- Python 3.8+
- Flask
- spaCy
- scikit-learn
- PyPDF2
- FPDF
- Bootstrap 5

---

## ⚡ Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/resume_analyser.git
   cd resume_analyser
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. **Run locally:**
   ```bash
   python app.py
   ```
   Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🌐 Production Deployment

- **Gunicorn:**
  ```bash
  gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
  ```
- **Nginx Reverse Proxy:** See sample config in the repo or documentation.
- **Free Hosting:** Try Render, Railway, or Fly.io for zero-cost deployment.

---

## 🔒 Security & Privacy
- Only PDF/TXT files up to 2MB are accepted.
- All resumes are deleted after analysis.
- No data is shared with third parties.

---

## 🤝 Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---
