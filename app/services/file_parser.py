import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
from typing import Union
from fastapi import UploadFile
import io
import openpyxl

def parse_file(file: UploadFile) -> str:
    filename = file.filename.lower()
    content = file.file.read()

    if filename.endswith(".txt"):
        return content.decode("utf-8")

    elif filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
        return df.to_string()

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))
        return df.to_string()

    elif filename.endswith(".html"):
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text()

    else:
        raise ValueError("Unsupported file type")
