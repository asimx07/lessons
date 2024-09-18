# Wikibuddy/models/vector_db.py

import faiss
import numpy as np
import pickle

class VectorDB:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, vectors, texts):
        self.index.add(np.array(vectors).astype('float32'))
        self.texts.extend(texts)

    def search(self, query_vector, k):
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), k)
        return [self.texts[i] for i in indices[0]]

    def save(self, filename):
        faiss.write_index(self.index, filename + ".index")
        with open(filename + ".texts", 'wb') as f:
            pickle.dump(self.texts, f)

    @classmethod
    def load(cls, filename):
        index = faiss.read_index(filename + ".index")
        db = cls(index.d)
        db.index = index
        with open(filename + ".texts", 'rb') as f:
            db.texts = pickle.load(f)
        return db
