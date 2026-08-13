from grammar_rag import rag_chain
from eval_dataset1 import test_cases


for case in test_cases:

    question = case["question"]
    expected = case["expected"]

    answer = rag_chain.invoke(question)

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("\nEXPECTED:")
    print(expected)

    print("\nRAG ANSWER:")
    print(answer)