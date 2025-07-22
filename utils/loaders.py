import fitz
import docx2txt
import email
from email import policy

def load_pdf(file_path):
    doc = fitz.open(file_path)
    return "".join([page.get_text() for page in doc])

def load_word(file_path):
    return docx2txt.process(file_path)

def load_email(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f, policy=policy.default)
        return msg.get_body(preferencelist=('plain')).get_content()
