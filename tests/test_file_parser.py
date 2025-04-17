from app.services.file_parser import parse_file
from fastapi import UploadFile
import io

class DummyUpload:
    def __init__(self, content, name):
        self.filename = name
        self.file = io.BytesIO(content.encode("utf-8"))

def test_parse_txt_file():
    dummy = DummyUpload("test content", "example.txt")
    result = parse_file(dummy)
    assert result == "test content"
