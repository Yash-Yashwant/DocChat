from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from src.config import settings

# Initialize resources once
embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL, google_api_key=settings.GOOGLE_API_KEY)
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query using dense embeddings."""
    
    # Perform similarity search
    retrieved_docs = vector_store.similarity_search(query, k=2)
    
    # Serialize results
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    
    return serialized, retrieved_docs
