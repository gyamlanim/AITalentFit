import os
import sys
from llm_interface import CustomLLM
import pysqlite3 as sqlite3
sys.modules["sqlite3"] = sqlite3
print("sqlite3 module version:", sqlite3.version)
print("SQLite engine version:", sqlite3.sqlite_version)
import chromadb
import uuid

class VectorDB:
    def __init__(self, db_location):
        # LLM interface for generating embeddings
        self.llm = CustomLLM()
        # Directory for ChromaDB storage
        self.db_path = db_location
        # ChromaDB persistent client instance
        self.client = chromadb.PersistentClient(path=self.db_path)
        # Log DB usage
        print("Using ChromaDB for vector similarity search")
       
    def create_table(self, table_name):
        # Create a collection for storing candidate documents and embeddings
        self.collection = self.client.get_or_create_collection(name=table_name)
    
    def insert_row(self, table_name, summary, full_resume, email, phone, name, candidate_id=None):
        # Auto-generate candidate_id if not provided
        if candidate_id is None:
            candidate_id = str(uuid.uuid4())
        # Generate embedding for the summary using LLM
        embedding = self.llm.get_embedding(summary)
        # Build metadata dictionary with all candidate info
        metadata = {
            "candidate_id": candidate_id,
            "full_resume": full_resume,
            "email": email,
            "phone": phone,
            "name": name
        }
        # Get or create the ChromaDB collection
        collection = self.client.get_or_create_collection(name=table_name)
        # Add candidate data to ChromaDB
        collection.add(
            ids=[candidate_id],
            documents=[summary],
            embeddings=[embedding],
            metadatas=[metadata]
        )
        return candidate_id

    def retrieve_top_results(self, table_name, top_n, job_description):
        # Generate embedding for the job description using LLM
        query_embedding = self.llm.get_embedding(job_description)
        # Get or create the ChromaDB collection
        collection = self.client.get_or_create_collection(name=table_name)
        # Get total number of documents in the collection
        total_docs = collection.count()
        # Use the smaller of top_n or available docs
        actual_n = min(top_n, total_docs) if total_docs > 0 else top_n
        # Query ChromaDB for top N most similar documents (summaries)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_n,
            include=['documents', 'distances', 'metadatas']
        )
        # Prepare formatted results list
        formatted_results = []
        # If there are results, process each one
        # IDs are returned automatically by ChromaDB, even without explicitly requesting them
        if results["documents"] and results["distances"]:
            for i, (summary, distance, metadata, candidate_id) in enumerate(zip(
                results["documents"][0],
                results["distances"][0],
                results["metadatas"][0],
                results["ids"][0]  # IDs are always available
            )):
                # Convert distance to similarity score (1 = perfect match, lower = less similar)
                similarity = 1 - distance
                # Add candidate info to results
                formatted_results.append({
                    "rank": i+1,
                    "candidate_id": candidate_id,
                    "summary": summary,
                    "similarity": similarity,
                    "metadata": metadata
                })
        # Return the list of top candidates
        return formatted_results

    def get_row_with_id(self, table_name, row_id):
        # Get a specific row from the ChromaDB collection by ID
        collection = self.client.get_or_create_collection(name=table_name)
        result = collection.get(ids=[row_id])
        return result