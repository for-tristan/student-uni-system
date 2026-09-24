from rag import ask_rag


questions = [
    "ما هي شروط التخرج من الكلية؟",
    "ما هو العبء الدراسي الاعتيادي المسموح به للطالب؟",
    "ما هي قواعد الامتحانات؟",
    "ما هي شروط التسجيل في المقررات؟",
    "ما هي متطلبات التخرج؟",
    "ما هو أفضل موبايل؟"
]


print("=" * 60)
print("        University FAQ Chatbot - Evaluation")
print("=" * 60)


for i, question in enumerate(questions, start=1):

    print(f"\n{'=' * 60}")
    print(f"Test {i}")
    print(f"Question: {question}")
    print("-" * 60)

    try:
        answer = ask_rag(question)
        print("Answer:")
        print(answer)

    except Exception as e:
        print("Error:")
        print(e)


print("\n" + "=" * 60)
print("Evaluation Finished")
print("=" * 60)
