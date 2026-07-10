import fitz  # PyMuPDF


def read_pdf(file_path):
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()