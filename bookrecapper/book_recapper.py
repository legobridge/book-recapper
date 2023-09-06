import time
from typing import List

import pandas as pd
import streamlit as st
from tqdm import tqdm

from chromadb_helper import ChromaDbHelper
from file_parser import extract_full_text
from palm_helper import PalmHelper


def divide_text_into_chunks(full_text: str, words_per_chunk: int = 500) -> List[str]:
    words = full_text.split()
    num_chunks = len(words) // words_per_chunk
    if len(words) % words_per_chunk != 0:
        num_chunks += 1
    chunks = []
    for i in range(num_chunks):
        lo = i * words_per_chunk
        hi = min(len(words), (i + 1) * words_per_chunk + 1)
        chunks.append(" ".join(words[lo:hi]))
    return chunks


def main():
    with st.form("Form"):
        palm_api_key = st.text_input("PaLM API Key")
        uploaded_file = st.file_uploader("Upload the book", type=["txt", "epub"])
        user_query = st.text_input(
            "What is the last thing you remember happening? "
            "Provide as much details as possible. "
            "Direct quotes are preferable."
        )
        num_candidates = st.slider(
            "Number of Search Results", min_value=1, max_value=20
        )

        query_submitted = st.form_submit_button("Submit Query")
        if query_submitted and uploaded_file is not None:
            palm_helper = PalmHelper(palm_api_key)
            chromadb_helper = ChromaDbHelper()
            full_text = extract_full_text(uploaded_file)
            text_chunks = divide_text_into_chunks(full_text, words_per_chunk=500)
            text_chunk_embeddings = []
            for chunk in tqdm(text_chunks):
                text_chunk_embeddings.append(palm_helper.generate_embedding(chunk))
                time.sleep(0.2)
            chromadb_helper.add_embeddings_to_collection(
                text_chunk_embeddings, text_chunks
            )

            query_embedding = palm_helper.generate_embedding(user_query)
            result_ids, result_documents = chromadb_helper.query_collection(
                query_embedding, num_candidates=num_candidates
            )
            df = pd.DataFrame.from_dict(
                {"result_ids": result_ids, "result_documents": result_documents}
            )
            st.dataframe(df)


if __name__ == "__main__":
    main()
