import sys
import os
from unittest import result

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import HumanMessage
from graph import graph


question = "What does obwohl mean?"

for event in graph.stream(
    {
        "messages": [
            HumanMessage(content=question)
        ]
    },
    config={
        "configurable": {
            "thread_id": "evaluation_1"
        }
    },
):

    print("\nEVENT:")
    print(event)