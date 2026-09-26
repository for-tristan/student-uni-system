# -*- coding: utf-8 -*-


import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


EXCEL_PATH = "university_faq_chunks.xlsx"     
DB_PATH = "./chroma_db"                      
COLLECTION_NAME = "university_faq"


EMBEDDING_MODEL = "intfloat/multilingual-e5-base"


def load_chunks(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    required_cols = {"chunk_id", "المصدر", "القسم / المادة", "رقم الصفحة", "النص"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"أعمدة ناقصة في الملف: {missing}")
    return df


def build_documents(df: pd.DataFrame):
    
    ids, documents, metadatas, embedding_inputs = [], [], [], []

    for _, row in df.iterrows():
        chunk_id = str(row["chunk_id"])
        source = str(row["المصدر"])
        section = str(row["القسم / المادة"])
        page = str(row["رقم الصفحة"])
        text = str(row["النص"])

        enriched_text = f"[{source} - {section}]\n{text}"

        text_for_embedding = f"passage: {enriched_text}"

        ids.append(f"chunk_{chunk_id}")
        documents.append(enriched_text) 
        embedding_inputs.append(text_for_embedding) 
        metadatas.append({
            "source": source,
            "section": section,
            "page": page,
        })

    return ids, documents, metadatas, embedding_inputs


def main():
    print("1) قراءة ملف الـ chunks...")
    df = load_chunks(EXCEL_PATH)
    print(f"   تم تحميل {len(df)} chunk.")

    print("2) تجهيز البيانات للتخزين...")
    ids, documents, metadatas, embedding_inputs = build_documents(df)

    print(f"3) تحميل موديل الـ embeddings ({EMBEDDING_MODEL})...")
    print("   (أول مرة هيحتاج إنترنت لتنزيل الموديل، بعد كده هيشتغل offline)")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("4) حساب الـ embeddings لكل الـ chunks...")
    embeddings = model.encode(embedding_inputs, show_progress_bar=True).tolist()

    print("5) إنشاء/فتح قاعدة بيانات Chroma...")
    client = chromadb.PersistentClient(path=DB_PATH)

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    print("6) تخزين الـ chunks في القاعدة...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\nتم بنجاح! القاعدة متخزنة في مجلد: {DB_PATH}")
    print(f"عدد الـ chunks المخزنة: {collection.count()}")

    print("\n--- تجربة بحث تجريبية ---")
    test_question = "ما هو العبء الدراسي الاعتيادي المسموح به للطالب؟"
    query_embedding = model.encode([f"query: {test_question}"]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
    )

    print(f"السؤال: {test_question}\n")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        print(f"نتيجة {i} — المصدر: {meta['source']} | القسم: {meta['section']} | صفحة: {meta['page']}")
        print(doc[:200] + "...\n")


if __name__ == "__main__":
    main()
