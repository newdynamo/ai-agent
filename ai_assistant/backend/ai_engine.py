import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import chromadb

# Load environment once at the top
load_dotenv()

class AIEngine:
    def __init__(self, chroma_path):
        # Reload env and get values inside __init__ to be safe
        load_dotenv()
        embedding_model = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
        llm_model = os.getenv("MODEL_NAME", "models/gemini-flash-latest")
        
        print(f"DEBUG: Using embedding model: {embedding_model}")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        self.llm_model = llm_model
        self.chroma_path = chroma_path
        self.vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=self.embeddings
        )

    def add_documents(self, pages_content):
        """
        Adds text and metadata (filename, page) to ChromaDB using small batches 
        and robust retry logic to stay within Gemini API free-tier limits.
        """
        batch_size = 2  # Reduced from 5 to avoid quota exhaustion for large docs
        for i in range(0, len(pages_content), batch_size):
            batch = pages_content[i:i + batch_size]
            texts = [p["text"] for p in batch]
            metadatas = [{"filename": p["filename"], "page": p["page"]} for p in batch]
            
            # Add current batch with improved retry logic for 429
            max_retries = 5  # Increased from 3
            for attempt in range(max_retries):
                try:
                    self.vector_store.add_texts(texts=texts, metadatas=metadatas)
                    break
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "ResourceExhausted" in error_str:
                        # Wait longer for free-tier quota resets
                        wait_time = 30 * (attempt + 1)
                        print(f"Quota exceeded. Retrying in {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(wait_time)
                        if attempt == max_retries - 1:
                            raise e
                    else:
                        raise e
            
            # Proactive sleep to stay within free-tier limits (RPM/TPM)
            if i + batch_size < len(pages_content):
                time.sleep(5)  # Increased from 3s to 5s


    def delete_document(self, filename):
        """
        Deletes documents from ChromaDB by filename.
        """
        # Retrieve IDs by metadata filtering
        results = self.vector_store.get(where={"filename": filename})
        if results["ids"]:
            self.vector_store.delete(ids=results["ids"])

    def get_answer(self, query):
        """
        Performs RAG and returns answer with citations.
        """
        prompt_template = """
        You are a helpful AI assistant. Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Always include the citation at the end of each relevant sentence or at the end of the paragraph.
        Citation format: [📄 filename, p.page_number]
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        chain = RetrievalQA.from_chain_type(
            llm=ChatGoogleGenerativeAI(model=self.llm_model, convert_system_message_to_human=True),
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = chain.invoke({"query": query})
        return result["result"], result["source_documents"]
