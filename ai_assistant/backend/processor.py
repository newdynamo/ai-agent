import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file page by page.
    Returns a list of dicts: [{"text": "...", "page": 1, "filename": "..."}]
    """
    doc = fitz.open(file_path)
    filename = os.path.basename(file_path)
    pages_content = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if text.strip():
            pages_content.append({
                "text": text,
                "page": page_num + 1,
                "filename": filename
            })
    
    doc.close()
    return pages_content
