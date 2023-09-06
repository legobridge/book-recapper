import streamlit as st

from bookrecapper.file_parser import extract_full_text


def main():
    uploaded_file = st.file_uploader("Upload the book", type=["txt", "epub"])
    if uploaded_file is not None:
        full_text = extract_full_text(uploaded_file)
        st.write(full_text)


if __name__ == "__main__":
    main()
