
from lc_config import store

QUESTIONS = [
    "What CGPA do I need to be eligible for placements?",
]


def search_handbook_questions():
    for query in QUESTIONS:
        print(f"\nQuestion: {query}")

        results = store.similarity_search(query, k=3)

        if not results:
            print("No results found.")
            continue

        for index, doc in enumerate(results, start=1):
            print(f"\nResult {index}")
            print(f"Source: {doc.metadata.get('source', 'unknown')}")
            print(doc.page_content)


if __name__ == "__main__":
    search_handbook_questions()
