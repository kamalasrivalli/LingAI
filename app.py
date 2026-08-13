import streamlit as st

from langchain_core.messages import HumanMessage
from graph import graph


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="LinguAI",
    page_icon="🗣️",
    layout="centered"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(" LinguAI")
st.caption("Your German AI language assistant")

st.markdown(
    """
    Ask about **German vocabulary and grammar**, or generate
    **practice exercises**.
    """
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "linguai_user"


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("LinguAI")

    st.markdown(
        """
        **Available tools**

        1. Dictionary lookup  
        2. German grammar RAG  
        3. Exercise generator
        """
    )

    st.divider()

    st.caption(
        "Built with Mistral, LangGraph, RAG and tool calling."
    )


# --------------------------------------------------
# Display conversation history
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------------
# Chat input
# --------------------------------------------------

question = st.chat_input(
    "Ask about German vocabulary, grammar, or practice..."
)


if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Run agent
    with st.chat_message("assistant"):

        with st.spinner("LinguAI is thinking..."):

            try:

                result = graph.invoke(
                    {
                        "messages": [
                            HumanMessage(content=question)
                        ]
                    },
                   
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }
                )

                answer = ""

                for message in reversed(result["messages"]):
                    if message.type == "ai" and message.content:
                        answer = message.content
                        break

                if not answer:
                    for message in reversed(result["messages"]):
                        if message.type == "tool" and message.content:
                            answer = message.content
                            break

            except Exception:
                answer = (
                    "Sorry, something went wrong while processing "
                    "your question. Please try again."
                )

        st.write(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })