
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

MODEL_PATH = r"D:\AI_fluency\models\all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_PATH,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

store = Chroma(
    collection_name="college_handbook",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
