import io
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Tuple

def parse_file(filename: str, content: bytes) -> Tuple[str, List[str]]:
    """
    Возвращает tuple: (тип_данных, список_чанков)
    тип_данных: 'text' или 'table'
    """
    ext = filename.lower().split(".")[-1]
    text = ""

    if ext == "pdf":
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = "\n".join([page.extract_text() or '' for page in pdf.pages])
        return "text", chunk_text(text)

    elif ext == "txt":
        text = content.decode("utf-8", errors="ignore")
        return "text", chunk_text(text)

    elif ext == "html":
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text()
        return "text", chunk_text(text)

    elif ext == "csv":
        df = pd.read_csv(io.BytesIO(content))
        return "table", df_to_rows(df)

    elif ext == "xlsx":
        df = pd.read_excel(io.BytesIO(content))
        return "table", df_to_rows(df)

    else:
        return "unknown", []

def chunk_text(text: str, max_len: int = 512) -> List[str]:
    return [text[i:i+max_len] for i in range(0, len(text), max_len) if text[i:i+max_len].strip()]

def df_to_rows(df: pd.DataFrame) -> List[str]:
    rows = df.fillna("").astype(str).apply(lambda row: " | ".join(row), axis=1).tolist()
    return rows