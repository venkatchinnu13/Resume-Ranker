import fitz  # PyMuPDF

def read_txt_file(file):
    return file.read().decode("utf-8")

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
