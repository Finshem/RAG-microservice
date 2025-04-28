# app/utils/file_types.py

# MIME types we support for text and HTML
TEXT_MIMES = {
    "text/plain",
    "text/html",
}

# MIME types we support for tabular data
TABLE_MIMES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# PDFs we also allow (we parse them as text)
ALL_MIMES = TEXT_MIMES | TABLE_MIMES | {
    "application/pdf",
}