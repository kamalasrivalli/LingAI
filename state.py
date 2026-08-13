from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class LinguAIState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    route: str