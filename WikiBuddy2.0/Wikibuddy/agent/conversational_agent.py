# Wikibuddy/agent/rag.py

import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from Wikibuddy.config import Config
from Wikibuddy.models.embedder import Embedder
from Wikibuddy.models.vector_db import VectorDB

class ConversationalAgent:
    def __init__(self):
        self.config = Config()
        self.embedder = Embedder(self.config.embedding_model)
        self.vector_db = VectorDB.load(self.config.vector_db_filename)
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=openai_api_key)
        self.conversation_history = []

    def get_completion(self, messages, max_tokens=350, temperature=0.1):
        response = self.client.chat.completions.create(
            model="gpt-4o",  # or whichever model you're using
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    def process_query(self, query):
        # Embed the query and search for relevant documents
        embedded_query = self.embedder.embed_query(query)
        search_results = self.vector_db.search(embedded_query, k=5)
        # Print retrieved documents
        print("Retrieved documents:")
        for i, result in enumerate(search_results, 1):
            print(f"Document {i}:")
            print(result[:200] + "..." if len(result) > 200 else result)
            print()

        # Prepare context from search results
        context = "\n".join([f"Relevant info {i+1}: {result}" for i, result in enumerate(search_results)])
        
        # Prepare messages for the API call
        messages = self.conversation_history + [
            {"role": "system", "content": f"You are a helpful assistant. Use the following information to answer the user's question:\n{context}"},
            {"role": "user", "content": query}
        ]
        
        # Get response from OpenAI
        response = self.get_completion(messages)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response})
        print(self.conversation_history)
        # Limit conversation history to last 10 messages to avoid token limit issues
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return response
