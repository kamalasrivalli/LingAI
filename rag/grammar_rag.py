from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

loader = PyMuPDFLoader(
    "german_grammar.pdf"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    encode_kwargs={
        "normalize_embeddings": True
    }
)

vectorstore = FAISS.from_documents(
    chunks,
    embeddings,
    distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

llm = ChatOllama(
    model="mistral",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a German grammar teacher.

Answer the question using ONLY the provided context.

If the answer cannot be found in the context, say:

"I cannot find the answer in the grammar book."

Context:
{context}

Question:
{question}
""")

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

def retrieve_docs(question):

    return retriever.invoke(question)

def rag_input(question):

    docs = retrieve_docs(question)

    return {
        "context": format_docs(docs),
        "question": question
    }

rag_chain = (
    rag_input
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":

    question = "When do I use obwohl?"

    response = rag_chain.invoke(question)

    print(response)