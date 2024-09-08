# Wikibuddy/models/vector_db.py
import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add(self, vectors):
        self.index.add(np.array(vectors).astype('float32'))

    def search(self, query_vector, k):
        return self.index.search(np.array([query_vector]).astype('float32'), k)

    def save(self, filename):
        faiss.write_index(self.index, filename)

    @classmethod
    def load(cls, filename):
        index = faiss.read_index(filename)
        db = cls(index.d)
        db.index = index
        return db
