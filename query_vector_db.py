# -*- coding: utf-8 -*-


import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "./chroma_db"
COLLECTION_NAME = "university_faq"
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"


def search(question: str, n_results: int = 3):
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer(EMBEDDING_MODEL)

    query_embedding = model.encode([f"query: {question}"]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)

    print(f"\nالسؤال: {question}\n" + "=" * 50)
    for i, (doc, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1
    ):
        print(f"\n[{i}] المصدر: {meta['source']} | القسم: {meta['section']} | صفحة: {meta['page']} | درجة التقارب: {1 - dist:.2f}")
        print(doc)

    return results


if __name__ == "__main__":
    search("ما هي شروط التخرج من الكلية؟")

