import requests
from langchain_core.tools import tool
from rag.grammar_rag import rag_chain
from llm import llm 


@tool(
    "dictionary_lookup",
     description=(
    "MANDATORY TOOL for German vocabulary. "
    "Use this tool whenever the user asks what a German word means, "
    "asks for its definition, or asks for its translation. "
    "Do NOT answer these questions directly."
    )
)
def dictionary_tool(word: str) -> str:
    """Look up a German word in German Wiktionary and return its dictionary entry."""

    word = word.strip()

    url = f"https://de.wiktionary.org/api/rest_v1/page/summary/{word}"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "LinguAI/1.0"},
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        extract = data.get("extract")

        if not extract:
            return f"I couldn't find '{word}' in the German Wiktionary."

        return f"Word: {word}\n\n{extract}"

    except requests.RequestException:
        return "Sorry, the dictionary service is currently unavailable."

    except (KeyError, TypeError):
        return "Sorry, I couldn't process the dictionary entry."

@tool(
    "german_grammar_search",
    description=(
        "Use this tool when the user asks how, when, or why a German "
        "grammatical form or construction is used. Also use it for "
        "questions about sentence structure, word order, cases, tenses, "
        "and grammar rules."
    )
)
def grammar_rag(question: str) -> str:
    """Answer German grammar questions using the German grammar book."""

    try:
        result = rag_chain.invoke(question)

        if not result:
            return "I couldn't find relevant information in the grammar book."

        return result

    except Exception:
        return "Sorry, I couldn't access the grammar knowledge base."


@tool(
    "exercise_generator",
    description=(
        "Generate German language exercises for a requested topic. "
        "Use this when the user asks for exercises, practice questions, "
        "a quiz, or practice sentences."
    )
)
def exercise_generator(topic: str) -> str:

    if not topic.strip():
        return "Please provide a topic for the exercise."

    prompt = f"""
Create a German language exercise about: {topic}.

Include:
- 5 questions
- Clear instructions
- An answer key at the end

Adapt the exercise to the topic requested by the user.
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception:
        return "Sorry, I couldn't generate the exercise right now."