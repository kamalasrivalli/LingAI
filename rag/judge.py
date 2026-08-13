from llm import llm
from grammar_rag import retriever, rag_chain
from eval_dataset import test_cases


def judge_answer(question, answer, context):

    prompt = f"""
You are evaluating a German grammar RAG system.

Question:
{question}

Retrieved context:
{context}

RAG answer:
{answer}

Evaluate the answer on three criteria:

1. Correctness: Is the answer factually correct?
2. Relevance: Does it answer the question directly?
3. Groundedness: Is the answer supported by the retrieved context?

Give each a score from 1 to 5.

Return exactly:

Correctness: X
Relevance: X
Groundedness: X
"""

    return llm.invoke(prompt).content


for case in test_cases:

    question = case["question"]

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    answer = rag_chain.invoke(question)

    evaluation = judge_answer(
        question,
        answer,
        context
    )

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("\nANSWER:", answer)
    print("\nJUDGE:")
    print(evaluation)