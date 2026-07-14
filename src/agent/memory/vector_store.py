"""Minimal keyword vector store for retrieval-augmented answers.

This is a dependency-free fallback (no numpy / faiss). It indexes documents
by token frequency and ranks by cosine similarity over the term vectors.
Suitable for small corpora on weak devices; swap for a real vector DB in the
optional layer when resources allow.
"""

import math
import re
from typing import Dict, List, Tuple


def _tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9_]+", text.lower()) if len(t) > 2]


class VectorStore:
    def __init__(self):
        self.docs: List[str] = []
        self.vectors: List[Dict[str, float]] = []

    def add(self, doc: str) -> int:
        vec = self._vector(_tokenize(doc))
        self.docs.append(doc)
        self.vectors.append(vec)
        return len(self.docs) - 1

    def search(self, query: str, top_k: int = 3) -> List[Tuple[int, float]]:
        if not self.vectors:
            return []
        qvec = self._vector(_tokenize(query))
        scored = [(i, self._cosine(qvec, v)) for i, v in enumerate(self.vectors)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def top_docs(self, query: str, top_k: int = 3) -> List[str]:
        return [self.docs[i] for i, _ in self.search(query, top_k)]

    @staticmethod
    def _vector(tokens: List[str]) -> Dict[str, float]:
        vec: Dict[str, float] = {}
        for t in tokens:
            vec[t] = vec.get(t, 0.0) + 1.0
        return vec

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        keys = set(a) | set(b)
        num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
        denom = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(
            sum(v * v for v in b.values())
        )
        return num / denom if denom else 0.0
