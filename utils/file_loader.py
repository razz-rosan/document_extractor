from PyPDF2 import PdfReader
import docx
import pytesseract
from PIL import Image
import io

# Set path to tesseract executable (only needed on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # adjust if needed

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

def extract_text(file, filename: str):
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file)
    else:
        # 🔥 Try content-type fallback if extension fails
        try:
            content_type = file.type  # e.g., 'image/png'
            if content_type == "application/pdf":
                return extract_text_from_pdf(file)
            elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return extract_text_from_docx(file)
            elif content_type == "text/plain":
                return file.read().decode("utf-8")
            elif content_type in ["image/jpeg", "image/png"]:
                return extract_text_from_image(file)
        except:
            pass

        raise ValueError("Unsupported file type")
