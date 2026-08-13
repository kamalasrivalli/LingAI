from langchain_core.messages import HumanMessage
from nodes import agent_chain

response = agent_chain.invoke({
    "messages": [
        HumanMessage(content="What does obwohl mean?")
    ]
})

print("CONTENT:")
print(response.content)

print("\nTOOL CALLS:")
print(response.tool_calls)