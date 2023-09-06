import os
from io import StringIO

from bs4 import BeautifulSoup
import ebooklib
import streamlit as st
from ebooklib import epub


def epub_html_chunk_to_str(html_chunk):
    soup = BeautifulSoup(html_chunk.get_body_content(), "html.parser")
    text = [para.get_text() for para in soup.find_all("p")]
    return "\n\n".join(text)


def main():
    uploaded_file = st.file_uploader("Upload the book", type=["txt", "epub"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith("txt"):
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            full_text = stringio.read()
            st.write(full_text)
        elif uploaded_file.name.endswith("epub"):
            uploaded_file_path = os.path.join("data", uploaded_file.name)
            with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            book = epub.read_epub(uploaded_file_path)
            full_text_chunks = []
            for html_chunk in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                full_text_chunks.append(epub_html_chunk_to_str(html_chunk))
            full_text = "\n\n<PAGEBREAK>\n\n".join(full_text_chunks)
            st.write(full_text)


if __name__ == "__main__":
    main()
