# LinguAI

Your German AI language assistant.

LinguAI is an agentic German language assistant that helps users learn German vocabulary and grammar and generate practice exercises.

The application combines Mistral, LangGraph, RAG, tool calling, prompt engineering, and Streamlit to create a multi-capability German language assistant.

## Features

- German vocabulary lookup
- German grammar question answering using RAG
- German exercise generation
- LLM-based tool selection
- Structured tool calling
- Stateful conversations
- Follow-up questions using conversation context
- Streamlit chat interface
- Local Mistral inference through Ollama
- Retrieval-augmented generation for German grammar

## Architecture

```mermaid
flowchart TD
    A[User] --> B[Streamlit UI]
    B --> C[LangGraph Agent]

    C --> D{Tool Selection}

    D --> E[Dictionary Tool]
    D --> F[German Grammar RAG]
    D --> G[Exercise Generator]

    F --> H[Retriever]
    H --> I[German Grammar Knowledge Base]

    E --> J[Tool Result]
    I --> J
    G --> J

    J --> C
    C --> K[Mistral]
    K --> B

Agent Workflow

The user submits a question through the Streamlit interface.

The LangGraph agent analyzes the user's intent and selects the appropriate capability:

Vocabulary questions → Dictionary Tool
Grammar questions → German Grammar RAG
Practice requests → Exercise Generator

The selected tool is executed and its result is returned to the agent. Mistral then uses the tool result to generate the final response.

The general workflow is:
User Question
      ↓
Streamlit
      ↓
LangGraph Agent
      ↓
Tool Selection
      ↓
Tool Execution
      ↓
Tool Result
      ↓
Mistral
      ↓
Final Answer

Tech Stack
Python
Mistral
Ollama
LangChain
LangGraph
Retrieval-Augmented Generation (RAG)
Streamlit
Vector search
Custom Python tools
Prompt engineering
Project Structure

LinguAI/
│
├── docs/
│
├── rag/
│
├── tests/
│   ├── agent_eval_test.py
│   └── agent_evaluation.py
│
├── agent.py
├── app.py
├── dictionary.py
├── graph.py
├── graph_learn.py
├── llm.py
├── memory.py
├── nodes.py
├── prompts.py
├── state.py
├── tools.py
├── test.py
├── temp.py
│
├── german_grammar.pdf
├── requirements.txt
└── README.md

Core Components
app.py

Provides the Streamlit user interface and manages the chat interaction.

agent.py

Defines the agent logic and LLM interaction.

graph.py

Defines the LangGraph workflow and connects the agent and tool execution.

nodes.py

Contains the graph nodes used in the agent workflow.

tools.py

Contains the tools available to the agent.

dictionary.py

Handles German dictionary lookup functionality.

prompts.py

Contains the prompts used to guide the LLM and tool selection.

state.py

Defines the state structure used by the LangGraph workflow.

memory.py

Handles conversation state and checkpointing.

llm.py

Configures the Mistral language model through Ollama.

german_grammar.pdf

Knowledge source used by the German grammar RAG system.

rag/

Contains components related to retrieval-augmented generation.

tests/

Contains experiments and tests for evaluating agent behavior and tool selection.

Installation

1. Clone the repository

git clone https://github.com/kamalasrivalli/LingAI
cd LinguAI

2. Create a virtual environment

python -m venv .venv

Activate the environment on macOS/Linux:

source .venv/bin/activate

On Windows:

.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Install Ollama

LinguAI currently uses Mistral locally through Ollama.

Install Ollama and make sure it is running.

Then download the Mistral model:

ollama pull mistral

5. Run the application

From the project directory:

streamlit run app.py

The application will open in your browser.

Example Usage
Vocabulary

Ask:

What does "gelten" mean?

LinguAI can use the dictionary tool to retrieve information about the German word.

Grammar

Ask:

When do I use "damit"?

The agent can route the question to the German grammar RAG system.

Follow-up Questions

LinguAI maintains conversation state, allowing follow-up questions such as:

What does gelten mean?

What is its past tense?

The second question can use the previous conversation context to understand what "its" refers to.

Exercises

Ask:

Give me a German verb conjugation exercise.

The exercise generator can create a German practice task.

Tool Calling

LinguAI uses LLM-based tool calling to connect the language model with external capabilities.

A typical interaction follows:

User
 ↓
Mistral / Agent
 ↓
Structured Tool Call
 ↓
Tool Execution
 ↓
Tool Result
 ↓
Mistral
 ↓
Final Answer

For example, a grammar question may result in a tool call similar to:

german_grammar_search(
    question="When do I use damit?"
)

The grammar tool retrieves relevant information from the knowledge base and returns the result to the agent.

The agent then uses the retrieved information to generate the final response.

Prompt Engineering

Prompt engineering is used to guide the agent's behavior and tool selection.

The agent prompt defines the purpose of each available tool and provides instructions for selecting the appropriate capability based on the user's intent.

The project also demonstrates how tool descriptions and system instructions influence LLM-based routing.

RAG Pipeline

The grammar component uses Retrieval-Augmented Generation to provide the language model with relevant information from the German grammar knowledge base.

The general pipeline is:

German Grammar Documents
        ↓
Document Processing
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Retrieval
        ↓
Relevant Context
        ↓
Mistral
        ↓
Grammar Answer

This allows the model to generate answers using retrieved information rather than relying entirely on its internal knowledge.

Conversation Memory

LinguAI uses LangGraph state and checkpointing to maintain conversation context.

This allows the application to handle follow-up questions and preserve relevant information across turns.

A conversation can therefore follow a pattern such as:

User: What does gelten mean?

Assistant: ...

User: What is its past tense?

Assistant: ...

Testing and Evaluation

The project includes experiments for evaluating agent behavior and tool selection in the tests/ directory.

The current evaluation work focuses on verifying whether the agent selects the appropriate tool for different types of questions.

Automated evaluation is still an area for improvement and is not currently presented as a production-grade benchmark.

Limitations
The application currently relies on a locally hosted Mistral model through Ollama.
Response quality depends on the underlying language model.
LLM-based tool selection may occasionally be imperfect.
The grammar system is limited to the information available in its knowledge base.
The current application is a learning/research prototype rather than a production-grade service.
No formal safety or guardrail layer has been implemented yet.
Automated evaluation and benchmarking are still being developed.
The application has not yet been containerized or exposed through a production API.
Future Improvements
Automated evaluation of tool selection and answer quality
Improved retrieval evaluation
Retrieval reranking
Guardrails and input/output validation
Prompt-injection and agent-security testing
Multilingual support
Fine-tuning and LoRA experiments
FastAPI backend
Docker containerization
Public cloud deployment
MCP-based tool integration
Improved observability and logging
More comprehensive evaluation datasets
Deployment

A public deployment is planned as the next stage of the project.

The application will be deployed so that users can interact with LinguAI without setting up the project locally.

Learning Outcomes

This project was built as a hands-on exploration of modern LLM application development.

Key concepts explored include:

Large Language Model integration
Prompt engineering
Tool calling
Structured tool calls
Agent workflows
LangGraph
Conversation state
Retrieval-Augmented Generation
Vector retrieval
Local LLM inference
Streamlit application development
Agent debugging and evaluation
Future Roadmap

The project will continue to evolve toward a more production-oriented LLM application.

Planned work includes:

Current LinguAI
      ↓
Public Deployment
      ↓
FastAPI Backend
      ↓
Docker
      ↓
Automated Evaluation
      ↓
Guardrails & Security
      ↓
Improved Agent Architecture

License

This project is intended for educational and research purposes.