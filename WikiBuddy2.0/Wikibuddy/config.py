# Wikibuddy/config.py
from dataclasses import dataclass, field

@dataclass
class Config:
    chunk_size: int = 3000
    chunk_overlap: int = 200
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_db_dimension: int = 384
    vector_db_filename: str = "vector_store.faiss"
    url_files: str = "wikilinks.txt"
