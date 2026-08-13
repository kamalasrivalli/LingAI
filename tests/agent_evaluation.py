import sys
import os
from unittest import result


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes import agent_chain

from langchain_core.messages import HumanMessage

from graph import graph


test_cases = [
    {
        "question": "What does gelten mean?",
        "expected_tool": "dictionary_lookup"
    },
    {
        "question": "What does obwohl mean?",
        "expected_tool": "dictionary_lookup"
    },
    {
        "question": "When do I use damit?",
        "expected_tool": "german_grammar_search"
    },
    {
        "question": "Explain German subordinate clauses.",
        "expected_tool": "german_grammar_search"
    },
    {
        "question": "Give me a B1 exercise about weil.",
        "expected_tool": "exercise_generator"
    },
]

failure_cases = [
    {
        "question": "What does xyzabc123 mean?",
        "expected_tool": "dictionary_lookup"
    },
    {
        "question": "Give me an exercise.",
        "expected_tool": "exercise_generator"
    },
    {
        "question": "What is the weather today?",
        "expected_tool": "none"
    },
]

def evaluate_agent():

    correct = 0

    for i, case in enumerate(test_cases):

        response = agent_chain.invoke({
            "messages": [
                HumanMessage(content=case["question"])
            ]
        })

        tool_calls = response.tool_calls

        actual_tool = (
            tool_calls[0]["name"]
            if tool_calls
            else "none"
        )

        expected_tool = case["expected_tool"]

        passed = actual_tool == expected_tool

        if passed:
            correct += 1

        print("\n" + "=" * 60)
        print("Question:", case["question"])
        print("Expected:", expected_tool)
        print("Actual:", actual_tool)
        print("Result:", "PASS" if passed else "FAIL")

    accuracy = correct / len(test_cases)

    print("\n" + "=" * 60)
    print(f"Tool Selection Accuracy: {accuracy:.0%}")

def evaluate_failure_cases():

    correct = 0

    for case in failure_cases:

        response = agent_chain.invoke({
            "messages": [
                HumanMessage(content=case["question"])
            ]
        })

        tool_calls = response.tool_calls

        actual_tool = (
            tool_calls[0]["name"]
            if tool_calls
            else "none"
        )

        expected_tool = case["expected_tool"]

        passed = actual_tool == expected_tool

        if passed:
            correct += 1

        print("\n" + "=" * 60)
        print("Question:", case["question"])
        print("Expected:", expected_tool)
        print("Actual:", actual_tool)
        print("Result:", "PASS" if passed else "FAIL")

    accuracy = correct / len(failure_cases)

    print("\n" + "=" * 60)
    print(f"Failure/Edge-case Accuracy: {accuracy:.0%}")


if __name__ == "__main__":
    evaluate_agent()
    evaluate_failure_cases()