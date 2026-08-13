# 🗣️ LinguAI

LinguAI is a German language assistant built with LangGraph, LangChain,
Mistral, Retrieval-Augmented Generation (RAG), and tool calling.

It helps users with German vocabulary, grammar, and language practice.

## Features

- German vocabulary lookup using German Wiktionary
- German grammar question answering using RAG
- German exercise generation
- LLM-based tool selection
- LangGraph agent workflow
- Conversation memory using a checkpointer
- Streamlit chat interface
- Agent tool-selection evaluation

## Architecture

```text
User
  │
  ▼
Streamlit
  │
  ▼
LangGraph Agent
  │
  ├── dictionary_lookup
  │       └── German Wiktionary
  │
  ├── german_grammar_search
  │       └── Grammar RAG pipeline
  │
  └── exercise_generator
          └── Mistral
  │
  ▼
Final Response