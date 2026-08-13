from tools import dictionary_tool
from tools import grammar_rag, exercise_generator
from llm import llm

llm_with_tools = llm.bind_tools(
    [
        dictionary_tool,
        grammar_rag,
        exercise_generator
    ],
    tool_choice="auto"
)