from typing import List, Tuple

from rank_bm25 import BM25Okapi


def tokenize(doc: str) -> List[str]:
    return doc.split()


class Bm25Helper:
    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        tokenized_corpus = [tokenize(doc) for doc in corpus]
        # todo - stemming/lemmatization?
        self.bm25 = BM25Okapi(tokenized_corpus)

    def query(self, query: str, num_candidates: int) -> Tuple[List[int], List[str]]:
        tokenized_query = tokenize(query)
        doc_scores_with_ids = [
            (score, i) for i, score in enumerate(self.bm25.get_scores(tokenized_query))
        ]
        sorted_doc_scores_with_ids = sorted(
            doc_scores_with_ids, reverse=True, key=lambda x: x[0]
        )
        sorted_doc_scores_with_ids = sorted_doc_scores_with_ids[:num_candidates]
        retrieved_ids = [x[1] for x in sorted_doc_scores_with_ids]
        retrieved_documents = [self.corpus[i] for i in retrieved_ids]
        return retrieved_ids, retrieved_documents
