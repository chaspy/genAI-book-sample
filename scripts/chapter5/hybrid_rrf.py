"""LangChain v1 で削除された EnsembleRetriever の簡易代替実装。

RRF（Reciprocal Rank Fusion）によって複数の Retriever を統合する。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Sequence, Tuple

from langchain_core.documents import Document


class ReciprocalRankFusion:
    """RRF スコアで複数 Retriever の結果を統合するシンプルな実装。"""

    def __init__(
        self,
        retrievers: Sequence,
        weights: Sequence[float] | None = None,
        rrf_k: int = 60,
    ) -> None:
        if not retrievers:
            raise ValueError("retrievers は1件以上必要です")

        if weights is None:
            weights = [1.0] * len(retrievers)

        if len(retrievers) != len(weights):
            raise ValueError("retrievers と weights の長さを揃えてください")

        self.retrievers = retrievers
        self.weights = weights
        self.rrf_k = rrf_k

    def invoke(self, query: str) -> list[Document]:
        """LangChain Retriever と同じインターフェースで結果を返す。"""
        scores: dict[Tuple[str | None, str], float] = defaultdict(float)
        documents: dict[Tuple[str | None, str], Document] = {}

        for weight, retriever in zip(self.weights, self.retrievers):
            candidates = retriever.invoke(query)
            for rank, doc in enumerate(candidates, start=1):
                key = (doc.metadata.get("source"), doc.page_content)
                documents.setdefault(key, doc)
                scores[key] += weight / (self.rrf_k + rank)

        fused = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [documents[key] for key, _ in fused]
