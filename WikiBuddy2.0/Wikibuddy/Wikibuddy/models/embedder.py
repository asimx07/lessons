# Wikibuddy/models/embedder.py
import logging
import asyncio
from transformers import AutoTokenizer, AutoModel
import torch

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, model_name):
        logger.info(f"Initializing Embedder with model: {model_name}")
        print(f"Initializing Embedder with model: {model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        logger.info("Embedder initialized successfully")
        print("Embedder initialized successfully")

    async def embed_docs(self, docs):
        logger.info(f"Starting to embed {len(docs)} documents")
        print(f"Starting to embed {len(docs)} documents")

        embeddings = []
        for i, doc in enumerate(docs):
            embedding = self.embed(doc)
            embeddings.append(embedding)

            if (i + 1) % 10 == 0 or (i + 1) == len(docs):  # Log every 10 docs or at the end
                logger.info(f"Embedded {i + 1}/{len(docs)} documents")
                print(f"Embedded {i + 1}/{len(docs)} documents")

        logger.info(f"Finished embedding {len(docs)} documents")
        print(f"Finished embedding {len(docs)} documents")

        return embeddings

    def embed_query(self, query):
        logger.info("Embedding query")
        print("Embedding query")

        embedding = self.embed(query)

        logger.info("Query embedding complete")
        print("Query embedding complete")

        return embedding

    def embed(self, text):
        logger.debug(f"Embedding text of length {len(text)}")

        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        logger.debug(f"Tokenized input shape: {inputs['input_ids'].shape}")

        with torch.no_grad():
            outputs = self.model(**inputs)

        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

        logger.debug(f"Generated embedding of length {len(embedding)}")

        return embedding
    
    

# If you want to test the file directly
if __name__ == "__main__":
    async def main():
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embedder = Embedder(model_name)

        # Test document embedding
        test_docs = [
            "This is a test document.",
            "Another test document with different content.",
            "A third document to embed."
        ]

        embeddings = await embedder.embed_docs(test_docs)

        print("\nTest Results:")
        print(f"Number of documents: {len(test_docs)}")
        print(f"Number of embeddings: {len(embeddings)}")
        print(f"Shape of first embedding: {len(embeddings[0])}")

        # Test query embedding
        test_query = "What is the capital of France?"
        query_embedding = embedder.embed_query(test_query)

        print(f"\nQuery: '{test_query}'")
        print(f"Shape of query embedding: {len(query_embedding)}")

    asyncio.run(main())
