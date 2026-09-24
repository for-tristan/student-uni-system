# -*- coding: utf-8 -*-

import chromadb
from sentence_transformers import SentenceTransformer




DB_PATH = "./chroma_db"
COLLECTION_NAME = "university_faq"
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"



client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(COLLECTION_NAME)

model = SentenceTransformer(EMBEDDING_MODEL)



def retrieve_context(question: str, n_results: int = 3):

    query_embedding = model.encode(
        [f"query: {question}"]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results



if __name__ == "__main__":

    question = "ما هي شروط التخرج من الكلية؟"

    results = retrieve_context(question)

    print("\nالسؤال:")
    print(question)

    print("\nأفضل النتائج:")
    print("=" * 60)

    for i, (doc, meta, distance) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ),
        1
    ):

        similarity = 1 - distance

        print(f"\nالنتيجة رقم {i}")
        print(f"المصدر: {meta['source']}")
        print(f"القسم: {meta['section']}")
        print(f"الصفحة: {meta['page']}")
        print(f"درجة التقارب: {similarity:.2f}")

        print("\nالنص:")
        print(doc)

        print("-" * 60)