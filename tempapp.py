from llm import llm_with_tools

response = llm_with_tools.invoke(
    "When does gelten mean?"
)

print(response)
print("\nTOOL CALLS:")
print(response.tool_calls)