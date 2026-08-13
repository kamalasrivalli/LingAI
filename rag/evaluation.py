from grammar_rag import retriever
from eval_dataset import test_cases


def evaluate_retrieval():

    results = []

    for case in test_cases:

        question = case["question"]
        expected = case["expected"]

        docs = retriever.invoke(question)

        context = " ".join(
            doc.page_content.lower()
            for doc in docs
        )

        found = [
            term for term in expected
            if term.lower() in context
        ]

        score = len(found) / len(expected)

        results.append({
            "question": question,
            "score": score,
            "found": found,
            "expected": expected
        })

    return results


if __name__ == "__main__":

    results = evaluate_retrieval()

    for result in results:

        print("\n" + "=" * 60)
        print("QUESTION:", result["question"])
        print("EXPECTED:", result["expected"])
        print("FOUND:", result["found"])
        print("SCORE:", result["score"])
        