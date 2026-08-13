from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import LinguAIState
from nodes import agent_node
from tools import dictionary_tool, grammar_rag, exercise_generator
from memory import memory


builder = StateGraph(LinguAIState)

builder.add_node("agent", agent_node)

builder.add_node(
    "tools",
    ToolNode([
        dictionary_tool,
        grammar_rag,
        exercise_generator
    ])
)


builder.add_edge(START, "agent")


def should_use_tool(state: LinguAIState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool"

    return "end"


builder.add_conditional_edges(
    "agent",
    should_use_tool,
    {
        "tool": "tools",
        "end": END
    }
)


builder.add_edge("tools", "agent")


graph = builder.compile(
    checkpointer=memory
)