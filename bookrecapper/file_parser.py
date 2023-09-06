import os
from io import StringIO

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def epub_html_chunk_to_str(html_chunk):
    soup = BeautifulSoup(html_chunk.get_body_content(), "html.parser")
    text = [para.get_text() for para in soup.find_all("p")]
    return "\n\n".join(text)


def extract_full_text(uploaded_file):
    if uploaded_file.name.endswith("txt"):
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        full_text = stringio.read()
    elif uploaded_file.name.endswith("epub"):
        uploaded_file_path = os.path.join("data", uploaded_file.name)
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        book = epub.read_epub(uploaded_file_path)
        full_text_chunks = []
        for html_chunk in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            full_text_chunks.append(epub_html_chunk_to_str(html_chunk))
        full_text = "\n\n<PAGEBREAK>\n\n".join(full_text_chunks)
    else:
        raise TypeError(f"Cannot parse file {uploaded_file.name}")
    return full_text
