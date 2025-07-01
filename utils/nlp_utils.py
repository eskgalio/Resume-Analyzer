import spacy
import json
import os
from PyPDF2 import PdfReader
import re

nlp = spacy.load('en_core_web_sm')

with open(os.path.join(os.path.dirname(__file__), 'job_roles.json'), 'r') as f:
    JOB_ROLES = json.load(f)

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def ats_compliance_check(text):
    issues = []
    if re.search(r'<table|<img', text, re.IGNORECASE):
        issues.append('Avoid using tables or images in your resume for ATS compliance.')
    if len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)) == 0:
        issues.append('No email address found. Add your contact email.')
    if len(re.findall(r'\b\d{10}\b', text)) == 0:
        issues.append('No phone number found. Add your contact number.')
    if len(text) > 10000:
        issues.append('Resume is too long. Keep it concise for ATS.')
    return issues

def score_resume(analysis, ats_issues):
    score = 100
    if len(analysis['skills']) < 5:
        score -= 20
    if not analysis['education']:
        score -= 15
    if not analysis['experience']:
        score -= 15
    score -= len(ats_issues) * 10
    if score < 0:
        score = 0
    return score

def analyze_resume(filepath):
    if filepath.endswith('.pdf'):
        text = extract_text_from_pdf(filepath)
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    doc = nlp(text)
    # Simple extraction: skills, education, experience (placeholder logic)
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
    education = [ent.text for ent in doc.ents if ent.label_ == 'EDUCATION']
    experience = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
    # Suggestions (placeholder)
    suggestions = []
    if len(skills) < 5:
        suggestions.append('Add more relevant skills.')
    if not education:
        suggestions.append('Include your education details.')
    if not experience:
        suggestions.append('Describe your work experience.')
    ats_issues = ats_compliance_check(text)
    score = score_resume({'skills': skills, 'education': education, 'experience': experience}, ats_issues)
    analysis = {
        'skills': skills,
        'education': education,
        'experience': experience,
        'text': text[:1000],  # preview
        'score': score,
        'ats_issues': ats_issues
    }
    return analysis, suggestions

def match_job_roles(analysis):
    # Simple keyword matching (placeholder)
    matches = []
    for role in JOB_ROLES:
        score = 0
        for skill in JOB_ROLES[role]['skills']:
            if skill.lower() in analysis['text'].lower():
                score += 1
        if score > 0:
            matches.append({'role': role, 'score': score})
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)
    return matches

def keyword_gap_analysis(resume_text, job_description):
    resume_words = set([w.lower() for w in re.findall(r'\w+', resume_text)])
    job_words = set([w.lower() for w in re.findall(r'\w+', job_description)])
    missing_keywords = list(job_words - resume_words)
    return missing_keywords 