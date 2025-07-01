from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from utils.nlp_utils import analyze_resume, match_job_roles, keyword_gap_analysis
from werkzeug.utils import secure_filename
from fpdf import FPDF
import logging

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_text(text):
    # Remove potentially dangerous characters
    return ''.join(c for c in text if c.isprintable())

@app.errorhandler(413)
def file_too_large(e):
    flash('File is too large. Max size is 2MB.')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        job_desc = request.form.get('job_desc', '')
        job_desc = sanitize_text(job_desc)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                logging.info(f'File uploaded: {filename}')
                return redirect(url_for('result', filename=filename, job_desc=job_desc))
            except Exception as ex:
                logging.error(f'Upload error: {ex}')
                flash('Error uploading file.')
                return redirect(request.url)
        else:
            flash('Invalid file type. Only PDF and TXT allowed.')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    job_desc = request.args.get('job_desc', '')
    job_desc = sanitize_text(job_desc)
    try:
        analysis, suggestions = analyze_resume(filepath)
        matches = match_job_roles(analysis)
        gap = []
        if job_desc:
            gap = keyword_gap_analysis(analysis['text'], job_desc)
        # Auto-delete file after analysis
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.info(f'File deleted: {filename}')
        return render_template('result.html', analysis=analysis, suggestions=suggestions, matches=matches, gap=gap, job_desc=job_desc, filename=filename)
    except Exception as ex:
        logging.error(f'Analysis error: {ex}')
        flash('Error analyzing resume.')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_report(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    analysis, suggestions = analyze_resume(filepath)
    matches = match_job_roles(analysis)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Resume Analysis Report', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Score: {analysis['score']}/100", ln=True)
    pdf.cell(0, 10, 'ATS Issues:', ln=True)
    for issue in analysis['ats_issues']:
        pdf.cell(0, 10, f"- {issue}", ln=True)
    pdf.cell(0, 10, 'Suggestions:', ln=True)
    for s in suggestions:
        pdf.cell(0, 10, f"- {s}", ln=True)
    pdf.cell(0, 10, 'Job Matches:', ln=True)
    for m in matches:
        pdf.cell(0, 10, f"- {m['role']} (Score: {m['score']})", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, 'Extracted Skills:', ln=True)
    for skill in analysis['skills']:
        pdf.cell(0, 10, f"- {skill}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, 'Education:', ln=True)
    for edu in analysis['education']:
        pdf.cell(0, 10, f"- {edu}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, 'Experience:', ln=True)
    for exp in analysis['experience']:
        pdf.cell(0, 10, f"- {exp}", ln=True)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_report.pdf")
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True) 