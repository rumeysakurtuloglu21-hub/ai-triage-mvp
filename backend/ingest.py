import os

# Hataları önlemek için
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def run_ingest():
    print(">>> İşlem başladı...") # Bu yazıyı görmelisin
    
    file_path = "saglik_rehberi.txt"
    
    if not os.path.exists(file_path):
        print(f"HATA: {file_path} bulunamadı!")
        return

    print(f"'{file_path}' okunuyor...")
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    print("Metin parçalara bölünüyor...")
    text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    print("Embedding modeli yükleniyor (Bu biraz sürebilir)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    print("ChromaDB'ye kaydediliyor...")
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print("="*30)
    print("BAŞARIYLA TAMAMLANDI!")
    print("="*30)

# BU KISIM ÇOK ÖNEMLİ:
if __name__ == "__main__":
    run_ingest()