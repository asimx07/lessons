# Wikibuddy/models/chunker.py
import logging
import asyncio
import os
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Chunker:
    def __init__(self, chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap
        logger.info(f"Initialized Chunker with chunk_size={chunk_size}, overlap={overlap}")
        print(f"Chunker initialized: chunk_size={chunk_size}, overlap={overlap}")
    
    @staticmethod
    def ensure_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")


    async def chunk(self, doc):
        logger.info(f"Starting to chunk document of length {len(doc)}")
        print(f"Chunking document of length {len(doc)}")

        chunks = []
        start = 0
        chunk_count = 0

        while start < len(doc):
            end = start + self.chunk_size
            chunk = doc[start:end]
            chunks.append(chunk)
            
            chunk_count += 1
            logger.debug(f"Created chunk {chunk_count}: start={start}, end={end}, length={len(chunk)}")
            
            if chunk_count % 10 == 0:  # Log every 10 chunks to avoid excessive logging
                logger.info(f"Created {chunk_count} chunks so far")
                print(f"Created {chunk_count} chunks so far")

            start = end - self.overlap

        logger.info(f"Finished chunking. Created {len(chunks)} chunks.")
        print(f"Chunking complete. Total chunks: {len(chunks)}")

        return chunks

    def save_chunks(self, chunks, index):
        self.ensure_dir("docs/chunks")
        filename = f"docs/chunks/article{index}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"Chunk{i}: {chunk}\n\n")
        logger.info(f"Saved {len(chunks)} chunks to {filename}")
