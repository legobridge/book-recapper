from typing import List, Tuple

import chromadb


class ChromaDbHelper:
    def __init__(self):
        self.chroma_client = chromadb.EphemeralClient()
        self.collection = self.chroma_client.create_collection(
            name="book_db", get_or_create=True
        )

    def add_embeddings_to_collection(
        self, embeddings: List[List[float]], documents: List[str]
    ):
        self.collection.add(
            ids=[str(i) for i in range(len(documents))],
            embeddings=embeddings,
            documents=documents,
        )

    def query_collection(
        self, query_embedding: List[float], num_candidates: int
    ) -> Tuple[List[str], List[str]]:
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=num_candidates
        )
        retrieved_ids = results["ids"][0]
        retrieved_documents = results["documents"][0]
        return retrieved_ids, retrieved_documents
