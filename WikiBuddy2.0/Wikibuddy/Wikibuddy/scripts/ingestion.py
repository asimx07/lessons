# scripts/ingestion.py
import asyncio
import logging
from Wikibuddy.config import Config
from Wikibuddy.models.data_source import Wikipedia
from Wikibuddy.models.chunker import Chunker
from Wikibuddy.models.embedder import Embedder
from Wikibuddy.models.vector_db import VectorDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ingest(config: Config):
    logger.info("Starting ingestion process")

    # Initialize components
    data_source = Wikipedia()
    chunker = Chunker(config.chunk_size, config.chunk_overlap)
    embedder = Embedder(config.embedding_model)
    vector_db = VectorDB(config.vector_db_dimension)

    # Fetch URLs
    urls = await data_source.gather_urls_from_file(config.url_files)
    logger.info(f"Fetched {len(urls)} URLs")

    # Fetch documents
    async with data_source:
        docs = await data_source.fetch(urls)
    logger.info(f"Fetched {len(docs)} documents")

    # Clean and chunk documents
    all_chunks = []
    for i, doc in enumerate(docs, 1):
        cleaned_doc = data_source._clean_docs(doc)
        data_source.save_cleaned_doc(cleaned_doc, i)
        
        chunks = await chunker.chunk(cleaned_doc)
        chunker.save_chunks(chunks, i)
        all_chunks.extend(chunks)

    logger.info(f"Created {len(all_chunks)} chunks in total")

    # Embed chunks
    embeddings = await embedder.embed_docs(all_chunks)
    logger.info(f"Created {len(embeddings)} embeddings")

    # Index embeddings and texts
    vector_db.add(embeddings, all_chunks)
    logger.info(f"Indexed {len(embeddings)} embeddings with their corresponding texts")

    # Save vector store
    vector_db.save(config.vector_db_filename)
    logger.info(f"Saved vector store to {config.vector_db_filename}")

if __name__ == "__main__":
    config = Config()
    asyncio.run(ingest(config))
