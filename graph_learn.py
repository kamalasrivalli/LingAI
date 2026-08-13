from langgraph.graph import StateGraph, START, END
from state import LinguAIState
from nodes import think_node, grammar_node, vocabulary_node
from memory import memory
from langgraph.prebuilt import ToolNode
from tools import dictionary_tool
from nodes import agent_node

tool_node = ToolNode(
    [dictionary_tool]
)

def should_use_tool(state: LinguAIState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool"

    return "end"

builder = StateGraph(LinguAIState)

builder.add_node("think", think_node)
builder.add_node("grammar", grammar_node)
builder.add_node("vocabulary", vocabulary_node)

builder.add_edge(START, "think")

builder.add_conditional_edges(
    "think",
    lambda state: state["route"],
    {
        "grammar": "grammar",
        "vocabulary": "vocabulary"
    }
)

builder.add_edge("grammar", END)
builder.add_edge("vocabulary", END)

graph = builder.compile(
    checkpointer=memory
)