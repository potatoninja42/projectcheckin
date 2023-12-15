from pdfminer.high_level import extract_text
import pandas as pd

def extract_pdf_data():
    text = extract_text()
    lines = text.split('\n')

    data = []
