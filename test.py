import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import pdf2image
from PIL import Image
import pytesseract
import cv2
from PyPDF2 import PdfReader
from docx import Document

DOCX_PARA_LIMIT = 1000 
TEXT_LIMIT = 5000
custom_config = r'--oem 1 --psm 11'
doc_dir = "/home/akshathprasad/Documents/Documents/Documents/"
model = SentenceTransformer("all-mpnet-base-v2")

if not os.path.exists('faiss_index.bin'):
    print("Initialising new faiss index")
    index = faiss.IndexFlatL2(768)
else:
    print("FAISS Index Loaded")
    index = faiss.read_index("faiss_index.bin")


if not os.path.exists("document_names.pkl"):
    print("Document Names not found")
    document_names = []
else:
    print("Document Names Loaded")
    with open("document_names.pkl", 'rb') as f:
        document_names = pickle.load(f)


def extract_text_pdf(path):
    reader = PdfReader(path)
    page = reader.pages[0]
    text = page.extract_text()
    return text


def extract_text_docx(path):
    doc = Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
        if len(text) > DOCX_PARA_LIMIT:
            break
    return '\n'.join(text)


def extract_text_txt(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text[:TEXT_LIMIT]


def extract_ocr(path):
    text = ""
    pages = pdf2image.convert_from_path(path)
    gray = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img = Image.fromarray(gray)
    text += pytesseract.image_to_string(img, lang="eng", config=custom_config) + "\n"
    return text


def extract_text_img(path):
    text = ""
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = Image.fromarray(gray)
    text += pytesseract.image_to_string(gray, lang="eng", config=custom_config) + '\n'


def extract_text_main(path):
    text = ""
    if path.lower().endswith('pdf'):
        text = extract_text_pdf(path)
        print(path, " Added!")
        if not text:
            text = extract_ocr(path)
        else:
            text = text + ' \n' + extract_ocr(path)
    elif path.lower().endswith('docx'):
        text = extract_text_docx(path)
        print(path, " Added!")
    elif path.lower().endswith('txt'):
        text = extract_text_txt(path)
        print(path, " Added!")
    elif path.lower().endswith(('jpg', 'png', 'jpeg')):
        text = extract_text_img(path)
        print(path, "Added!")
    return text


for file in os.listdir(doc_dir):
    path = os.path.join(doc_dir, file)
    if os.path.isdir(path):
        continue
    if path in document_names:
        continue
    text = extract_text_main(path)
    if text:
        text = text.lower()
    else:
        text = ""
    text = file + '\n' + text
    embedding = model.encode([text], normalize_embeddings=True)
    document_names.append(path)
    index.add(np.array(embedding, dtype=np.float32))
    with open("document_names.pkl", 'wb') as f:
        pickle.dump(document_names, f)

    faiss.write_index(index, "faiss_index.bin")
