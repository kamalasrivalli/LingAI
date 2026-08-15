# Building an Agentic RAG Application with LangGraph

This tutorial walks through the architecture and implementation of **LinguAI**, a German AI language assistant built with Mistral, LangChain, LangGraph, RAG, tool calling, and Streamlit.

The goal is not just to build a chatbot, but to understand how an LLM can:

- decide which tool to use
- call specialized tools
- retrieve external knowledge using RAG
- process tool results
- generate a final answer
- maintain conversational state

---

## 1. From an LLM to an Agent

A basic LLM application follows a simple pattern:

User question → LLM → Answer

For example:

```text
User
 ↓
LLM
 ↓
Answer

However, an LLM by itself does not automatically have access to a dictionary, database, search engine, or other external functionality.

An agent extends this architecture:

User
 ↓
Agent
 ↓
Choose a tool
 ↓
Execute the tool
 ↓
Receive the result
 ↓
Agent
 ↓
Final answer

## 2. LinguAI Architecture

LinguAI provides three main capabilities:

German vocabulary lookup
German grammar retrieval using RAG
German exercise generation

The high-level architecture is:

                    User
                     │
                     ▼
                  Mistral
                     │
               Tool selection
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Dictionary   Grammar    Exercise
         Tool        RAG       Generator
          │          │          │
          └──────────┼──────────┘
                     ▼
                  ToolNode
                     │
                     ▼
                  Mistral
                     │
                     ▼
                Final Answer
                     │
                     ▼
                 Streamlit

The important idea is that the LLM decides what needs to be done, while the tools perform the actual operations.

---

## 3. State and Messages

LangGraph applications need a way to store information as the graph executes.

For LinguAI, we define the state using `TypedDict`:

```python
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class LinguAIState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    route: str