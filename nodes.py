from state import LinguAIState
from prompts import router_prompt, grammar_prompt, vocabulary_prompt, agent_prompt
from llm import llm
from langchain_core.output_parsers import StrOutputParser
from agent import llm_with_tools
from langchain_core.messages import AIMessage, HumanMessage

parser = StrOutputParser()

router_chain = router_prompt | llm | parser
grammar_chain = grammar_prompt | llm | parser
vocabulary_chain = vocabulary_prompt | llm | parser
agent_chain = agent_prompt | llm_with_tools

def think_node(state: LinguAIState):

    route = router_chain.invoke(
        {
            "messages": state["messages"]
        }
    ).strip().lower()

    if "vocabulary" in route:
        route = "vocabulary"
    elif "grammar" in route:
        route = "grammar"
    else:
        raise ValueError(f"Invalid route returned by LLM: {route}")

    return {
        "route": route
    }

def grammar_node(state: LinguAIState):

    response = grammar_chain.invoke(
        {
             "messages": state["messages"]
        }
    )

    return {
    "messages": [
        AIMessage(content=response)
    ]
}

def vocabulary_node(state: LinguAIState):

    response = vocabulary_chain.invoke(
        {
             "messages": state["messages"]
        }
    )

    return {
    "messages": [
        AIMessage(content=response)
    ]
}

import json


def agent_node(state: LinguAIState):

    response = agent_chain.invoke({
        "messages": state["messages"]
    })

    content = response.content

    if isinstance(content, str):

        try:
            if "[TOOL_CALLS]" in content:
                tool_text = content.split("[TOOL_CALLS]", 1)[1].strip()

            elif "german_grammar_search" in content:
                start = content.find("[")
                end = content.rfind("]") + 1
                tool_text = content[start:end]

            elif "dictionary_lookup" in content:
                start = content.find("[")
                end = content.rfind("]") + 1
                tool_text = content[start:end]

            elif "exercise_generator" in content:
                start = content.find("[")
                end = content.rfind("]") + 1
                tool_text = content[start:end]

            else:
                tool_text = None

            if tool_text:
                calls = json.loads(tool_text)

                response.tool_calls = [
                    {
                        "name": call["name"],
                        "args": call["arguments"],
                        "id": f"call_{i}",
                        "type": "tool_call",
                    }
                    for i, call in enumerate(calls)
                ]

                response.content = ""

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass

    return {
        "messages": [response]
    }