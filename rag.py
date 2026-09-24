# -*- coding: utf-8 -*-

import os
from groq import Groq
from retrieval import retrieve_context



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)



def ask_rag(question: str):

    results = retrieve_context(question, n_results=3)

    context_parts = []

    for doc, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        context_parts.append(
            f"""
المصدر: {meta['source']}
القسم: {meta['section']}
الصفحة: {meta['page']}

النص:
{doc}
"""
        )

    context = "\n".join(context_parts)

    system_prompt = """
أنت مساعد ذكي خاص بالجامعة.

مهمتك الإجابة عن أسئلة الطلاب المتعلقة فقط بـ:

- University Rules
- Courses
- Exam Rules
- Sign-up Rules
- Graduation Requirements

استخدم المعلومات الموجودة في الـ Context فقط.

ممنوع اختراع أي معلومة أو قاعدة غير موجودة في الـ Context.

إذا لم تجد إجابة واضحة في الـ Context، قل:
"عذرًا، لم أجد هذه المعلومة في قاعدة بيانات الجامعة."

أجب باللغة العربية بشكل واضح ومختصر.

اذكر المصدر والصفحة إذا كانت المعلومات متاحة.
"""

    user_prompt = f"""
السؤال:
{question}

Context من قاعدة بيانات الجامعة:
{context}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# Chat Loop

if __name__ == "__main__":

    print("=" * 60)
    print("      University FAQ Chatbot")
    print("=" * 60)

    print("\nاكتب سؤالك عن الجامعة.")
    print("لإنهاء البرنامج اكتب: exit\n")

    while True:

        question = input("أنت: ")

        if question.lower() == "exit":
            print("\nتم إنهاء البرنامج.")
            break

        if not question.strip():
            print("من فضلك اكتب سؤالًا.\n")
            continue

        try:
            answer = ask_rag(question)

            print("\nالبوت:")
            print("-" * 60)
            print(answer)
            print("-" * 60)
            print()

        except Exception as e:
            print("\nحدث خطأ:")
            print(e)
            print()