from .base import BaseEmbedder
from .simple_transformer import SimpleTransformerEmbedder


def get_embedder(embedder_type: str = "transformer") -> BaseEmbedder:
    if embedder_type == "transformer":
        return SimpleTransformerEmbedder()
    else:
        raise ValueError(f"Unsupported embedder type: {embedder_type}")
