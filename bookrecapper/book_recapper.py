from typing import List

import pandas as pd
import streamlit as st

from bm25_helper import Bm25Helper
from chromadb_helper import ChromaDbHelper
from file_parser import extract_full_text
from palm_helper import PalmHelper

BM25 = "BM25"
VECTOR_SEARCH = "Vector Search"
QUERY_PROMPTS = {
    BM25: "Provide direct quotes from the last part you read.",
    VECTOR_SEARCH: "What is the last thing you remember happening? Provide as "
    "much detail as possible. Direct quotes are preferable. ",
}


def divide_text_into_chunks(full_text: str, words_per_chunk: int = 200) -> List[str]:
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


def summarize_chunks(palm_helper: PalmHelper, chunks: List[str]) -> str:
    summaries: List[str] = []
    progress_text = "Summarizing book chunks..."
    progress_bar = st.progress(0.0, text=progress_text)
    for i, chunk in enumerate(chunks):
        prompt = (
            f"Summarize the following text enclosed within triple backticks "
            f"in 100-200 words."
            f"\n```\n{chunk}\n```\n"
            f"Ignore meta text like table of contents, acknowledgements, "
            f"preface, etc. and only focus on the core content. "
            f"Return only the generated summary and nothing else. "
            f"Refer only to the content in the provided text and "
            f"don't spoil anything from future chapters. "
            f"Don't talk about the book, only about the "
            f"text provided within triple backticks. "
            f"The summary must be between 100-200 words long. "
        )
        completion = palm_helper.complete_prompt(prompt=prompt)
        summaries.append(completion)
        progress_bar.progress((i + 1) / len(chunks), text=progress_text)

    joined_summaries = "\n".join(summaries)
    prompt = (
        f"Summarize the following text within triple backticks "
        f"in around 500 words. "
        f"\n```\n{joined_summaries}\n```\n"
        f"Return only the generated summary and nothing else. "
        f"Refer only to the content in the provided text and "
        f"don't spoil anything from future chapters. "
        f"Don't talk about the book, only about the "
        f"text provided within triple backticks. "
        f"The summary must be around 500 words long. "
    )
    completion = palm_helper.complete_prompt(prompt=prompt)
    return completion


def generate_and_store_embeddings(
    chromadb_helper: ChromaDbHelper, palm_helper: PalmHelper, text_chunks: List[str]
):
    text_chunk_embeddings = []
    progress_text = "Generating embeddings for book chunks..."
    progress_bar = st.progress(0.0, text=progress_text)
    for i, chunk in enumerate(text_chunks):
        text_chunk_embeddings.append(palm_helper.generate_embedding(chunk))
        progress_bar.progress((i + 1) / len(text_chunks), text=progress_text)
    chromadb_helper.add_embeddings_to_collection(text_chunk_embeddings, text_chunks)


def main():
    # Ask the user for a PaLM API key
    palm_api_key = st.text_input("PaLM API Key")

    # Embedding Vector Search or BM25?
    search_algo = st.radio("Select Search Algorithm", options=[VECTOR_SEARCH, BM25])

    # Book upload widget
    uploaded_file = st.file_uploader("Upload the book", type=["txt", "epub"])

    if palm_api_key != "" and uploaded_file is not None:
        # Initialize PaLM Helper
        palm_helper = PalmHelper(palm_api_key)

        # Extract text
        full_text = extract_full_text(uploaded_file)

        # If there hasn't been a change in the uploaded file,
        # don't redo preprocessing
        file_changed = True
        if (
            "full_text" in st.session_state
            and full_text == st.session_state["full_text"]
        ):
            file_changed = False

        if file_changed:
            st.session_state["full_text"] = full_text
            st.session_state["text_chunks"] = divide_text_into_chunks(
                st.session_state["full_text"], words_per_chunk=200
            )

            # Preprocess search corpus
            if search_algo == VECTOR_SEARCH:
                st.session_state["chromadb_helper"] = ChromaDbHelper()
                generate_and_store_embeddings(
                    st.session_state["chromadb_helper"],
                    palm_helper,
                    st.session_state["text_chunks"],
                )
            elif search_algo == BM25:
                st.session_state["bm25_helper"] = Bm25Helper(
                    st.session_state["text_chunks"]
                )
            else:
                raise NotImplementedError(
                    f"Search Algorithm {search_algo} is not implemented."
                )

        with st.form("Query Form"):
            text_chunks = st.session_state["text_chunks"]
            user_query = st.text_input(QUERY_PROMPTS[search_algo])
            num_candidates = st.slider(
                "Number of Search Results", min_value=1, max_value=20, value=5
            )

            query_submitted = st.form_submit_button("Submit Query")
            if query_submitted:
                if search_algo == VECTOR_SEARCH:
                    chromadb_helper = st.session_state["chromadb_helper"]
                    query_embedding = palm_helper.generate_embedding(user_query)
                    result_ids, result_documents = chromadb_helper.query_collection(
                        query_embedding, num_candidates=num_candidates
                    )
                elif search_algo == BM25:
                    bm25_helper = st.session_state["bm25_helper"]
                    result_ids, result_documents = bm25_helper.query(
                        user_query, num_candidates=num_candidates
                    )
                else:
                    raise NotImplementedError(
                        f"Search Algorithm {search_algo} is not implemented."
                    )

                df = pd.DataFrame.from_dict(
                    {"result_ids": result_ids, "result_documents": result_documents}
                )
                st.dataframe(df)
                top_segment_id = int(df["result_ids"].iloc[0])
                combined_text_read_so_far = " ".join(text_chunks[:top_segment_id])
                bigger_chunks = divide_text_into_chunks(
                    combined_text_read_so_far, words_per_chunk=1000
                )
                st.write(summarize_chunks(palm_helper, bigger_chunks))


if __name__ == "__main__":
    main()
