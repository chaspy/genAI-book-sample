"""LangChain v1 で削除された EnsembleRetriever の簡易代替実装。

RRF（Reciprocal Rank Fusion）によって複数の Retriever を統合する。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Sequence, Tuple

from langchain_core.documents import Document


class ReciprocalRankFusion:
    """RRF スコアで複数 Retriever の結果を統合するシンプルな実装。

    LangChain v1 の LCEL で使いやすいように、Retriever にそろえた
    `invoke()` インターフェースだけを実装している。
    """

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
        # (source, page_content) をキーにしてスコアを累積する。
        scores: dict[Tuple[str | None, str], float] = defaultdict(float)
        # 最終的な Document をここに保持し、重複排除を行う。
        documents: dict[Tuple[str | None, str], Document] = {}

        for weight, retriever in zip(self.weights, self.retrievers):
            # Retriever を順に呼び出し、rank（1 始まり）を付けて RRF スコアを算出。
            candidates = retriever.invoke(query)
            for rank, doc in enumerate(candidates, start=1):
                key = (doc.metadata.get("source"), doc.page_content)
                documents.setdefault(key, doc)
                # RRF: weight / (k + rank) を足し合わせる。k は高順位をどれだけ重視するかの調整係数。
                scores[key] += weight / (self.rrf_k + rank)

        # スコアの高い順に並べ替えて Document のリストを返す。
        fused = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [documents[key] for key, _ in fused]
