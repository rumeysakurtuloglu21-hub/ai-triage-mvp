from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


def get_medical_context(query: str):
    try:
        docs = vector_db.similarity_search(query, k=2)

        if not docs:
            return ""

        return "\n".join(doc.page_content for doc in docs)

    except Exception as e:
        print("RAG ERROR:", e)
        return ""