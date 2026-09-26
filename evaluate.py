
# -*- coding: utf-8 -*-

from rag import ask_rag


# ==========================================
# 1. Test Cases
# ==========================================

test_cases = [
    {
        "question": "ما هي شروط التخرج من الكلية؟",
        "expected": ["الساعات", "نقطتين", "50"],
        "test_type": "normal"
    },
    {
        "question": "ما هو العبء الدراسي الاعتيادي المسموح به للطالب؟",
        "expected": ["6", "19"],
        "test_type": "normal"
    },
    {
        "question": "ما هي قواعد الامتحانات؟",
        "expected": ["الامتحان"],
        "test_type": "normal"
    },
    {
        "question": "ما هي شروط التسجيل في المقررات؟",
        "expected": ["التسجيل", "الساعات"],
        "test_type": "normal"
    },
    {
        "question": "ما هي متطلبات التخرج؟",
        "expected": ["الساعات", "نقطتين"],
        "test_type": "normal"
    },
    {
        "question": "ما هو أفضل موبايل؟",
        "expected": ["لم أجد هذه المعلومة"],
        "test_type": "out_of_scope"
    },
    {
        "question": "عايزة أعرف الطالب يسجل كام ساعة في الترم العادي؟",
        "expected": ["6", "19"],
        "test_type": "normal"
    },
    {
        "question": "ما هي شروط النجاح في التخرج؟",
        "expected": ["الساعات", "نقطتين"],
        "test_type": "normal"
    }
]


# ==========================================
# 2. Text Normalization
# ==========================================

def normalize_text(text):

    text = text.lower()

    # Normalize Arabic letters
    text = (
        text.replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .replace("ـ", "")
    )

    # Normalize percentage symbol
    text = text.replace("٪", "%")

    # Remove spaces and common punctuation
    for char in [
        " ", "\n", "\t",
        ".", ",", "،",
        ":", ";", "؛",
        "-", "_",
        "(", ")", "[", "]",
        "*", "ـ"
    ]:
        text = text.replace(char, "")

    return text


# ==========================================
# 3. Evaluation
# ==========================================

passed = 0
failed = 0
errors = 0

total = len(test_cases)

print("=" * 60)
print("      University FAQ Chatbot - Evaluation")
print("=" * 60)


for i, test in enumerate(test_cases, start=1):

    question = test["question"]
    expected = test["expected"]
    test_type = test["test_type"]

    print(f"\n{'=' * 60}")
    print(f"Test {i}/{total}")
    print(f"Question: {question}")
    print("-" * 60)

    try:

        # Get chatbot answer
        answer = ask_rag(question)

        print("\nAnswer:")
        print(answer)

        # Normalize answer
        normalized_answer = normalize_text(answer)

        # Normalize expected keywords
        normalized_expected = [
            normalize_text(word)
            for word in expected
        ]

        # Check answer
        if test_type == "out_of_scope":

            # The chatbot should refuse
            if all(
                word in normalized_answer
                for word in normalized_expected
            ):
                status = "PASS"
            else:
                status = "FAIL"

        else:

            matched_keywords = [
                expected[j]
                for j, word in enumerate(normalized_expected)
                if word in normalized_answer
            ]

            print("\nExpected keywords:", expected)
            print("Matched keywords:", matched_keywords)

            if len(matched_keywords) == len(expected):
                status = "PASS"
            else:
                status = "FAIL"

        # Count results
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\nTest Result: {status}")

    except Exception as e:

        errors += 1
        failed += 1

        print("\nError:")
        print(e)

        print("Test Result: ERROR")


# ==========================================
# 4. Final Evaluation Report
# ==========================================

success_rate = (passed / total) * 100 if total > 0 else 0

print("\n" + "=" * 60)
print("              FINAL EVALUATION REPORT")
print("=" * 60)

print(f"Total Tests : {total}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print(f"Errors      : {errors}")

print(f"Success Rate: {success_rate:.2f}%")

print("=" * 60)
print("Evaluation Finished")
print("=" * 60)