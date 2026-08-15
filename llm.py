import os

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


if os.getenv("HF_TOKEN"):

    llm_endpoint = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0,
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    )

    llm = ChatHuggingFace(llm=llm_endpoint)

else:

    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="mistral",
        temperature=0
    )