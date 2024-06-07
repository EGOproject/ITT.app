import os
from cryptography.fernet import Fernet
from docx import Document
from fpdf import FPDF

JOBS_FOLDER = "jobs"
KEY_FILE = "key.key"

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as file:
            file.write(key)
    return key

def initialize_cipher():
    key = load_or_generate_key()
    return Fernet(key)

cipher = initialize_cipher()

JOBS_FOLDER = "jobs"

def save_as_word(text, file_path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(file_path)

def save_as_pdf(text, file_path):
    try:
        # Replace problematic characters
        text = text.replace('\u2019', "'")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(file_path)
        print("PDF saved successfully.")
    except Exception as e:
        print(f"Error saving PDF: {e}")


def save_as_text(text, file_path):
    with open(file_path, 'w') as file:
        file.write(text)

def save_as_itt(text, job_name):
    if not os.path.exists(JOBS_FOLDER):
        os.makedirs(JOBS_FOLDER)
    
    file_path = os.path.join(JOBS_FOLDER, f"{job_name}.itt")
    encrypted_text = cipher.encrypt(text.encode())
    
    with open(file_path, 'wb') as file:
        file.write(encrypted_text)

def load_previous_jobs():
    if not os.path.exists(JOBS_FOLDER):
        return []
    
    jobs = []
    for file_name in os.listdir(JOBS_FOLDER):
        if file_name.endswith('.itt'):
            job_name = file_name[:-2]
            file_path = os.path.join(JOBS_FOLDER, file_name)
            with open(file_path, 'rb') as file:
                encrypted_text = file.read()
                decrypted_text = cipher.decrypt(encrypted_text).decode()
                jobs.append({
                    'name': job_name,
                    'text': decrypted_text,
                    'path': file_path
                })
    return jobs

def save_job(text):
    job_name = " ".join(text.split()[:1])  # Use the first word as the job name
    save_as_itt(text, job_name)
    return job_name
