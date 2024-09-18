# Wikibuddy/models/data_source.py
import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import re
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataSource:
    def __init__(self):
        self.session = None
        print(f"Initialized {self.__class__.__name__} instance")

    async def fetch(self, urls):
        """Fetch docs from source"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            print("Created new aiohttp ClientSession")
        
        print(f"Fetching {len(urls)} URLs")
        tasks = [self.fetch_url(url) for url in urls] 
        results = await asyncio.gather(*tasks)
        print(f"Fetched {len(results)} documents")
        return results

    async def fetch_url(self, url):
        logger.debug(f"Fetching URL: {url}")
        async with self.session.get(url) as response:
            text = await response.text()
            logger.debug(f"Fetched {len(text)} characters from {url}")
            return text
        
    @staticmethod
    def ensure_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

    @staticmethod
    async def gather_urls_from_file(filename):
        """Read URLs from files and return them as a list."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, filename)
        print(f"Reading URLs from file: {full_path}")
        
        urls = []
        try:
            with open(full_path, 'r') as file:
                for line in file:
                    urls.append(line.strip())
            print(f"Read {len(urls)} URLs from file")
        except FileNotFoundError:
            logger.error(f"File not found: {full_path}")
            raise
        except IOError as e:
            logger.error(f"IO error when reading file {full_path}: {str(e)}")
            raise
        
        return urls

    @staticmethod
    def _clean_docs(doc):
        logger.debug(f"Cleaning document of length {len(doc)}")
        soup = BeautifulSoup(doc, 'html.parser')
        cleaned = soup.get_text()
        
        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        logger.debug(f"Cleaned document to length {len(cleaned)}")
        return cleaned


    async def __aenter__(self):
        print(f"Entering context for {self.__class__.__name__}")
        return self

    def save_cleaned_doc(self, doc, index):
        self.ensure_dir("docs/articles")
        filename = f"docs/articles/article{index}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc)
        logger.info(f"Saved cleaned document to {filename}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            print("Closed aiohttp ClientSession")
        print(f"Exiting context for {self.__class__.__name__}")

class Wikipedia(DataSource):
    def __init__(self):
        super().__init__()
        print("Initialized Wikipedia data source")

class NYTimes(DataSource):
    def __init__(self):
        super().__init__()
        print("Initialized NYTimes data source")
 



