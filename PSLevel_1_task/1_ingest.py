
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_config import store

DATA_DIR = Path(__file__).parent / "data"


def ingest_documents():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()

    if not documents:
        print("No Markdown documents found.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    # Stable IDs prevent duplicate chunks during repeated ingestion.
    ids = []
    for index, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        ids.append(f"{Path(source).name}-{index}")

    store.add_documents(chunks, ids=ids)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print("Ingestion completed successfully.")


if __name__ == "__main__":
    ingest_documents()
