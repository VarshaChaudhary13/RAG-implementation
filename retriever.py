# -*- coding: utf-8 -*-
"""Untitled71.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rXTFwjIIMwQYIRyAK7Nuk_X5MRHYFjWE
"""

pip install langchain_community

pip install pypdf

from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("attention.pdf")
docs = loader.load()
docs

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
text_splitter.split_documents(docs)[:5]

documents=text_splitter.split_documents(docs)
documents

pip install sentence-transformers

!pip install faiss-cpu

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Use a Hugging Face model for embeddings, for example, all-MiniLM-L6-v2
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create the FAISS vector store with Hugging Face embeddings
db = FAISS.from_documents(documents[:30], hf_embeddings)

query="An attention function can be described as mapping a query "
result=db.similarity_search(query)
result[0].page_content

from langchain_community.llms import Ollama
## Load Ollama LAMA2 LLM model
llm=Ollama(model="llama2")
llm

from langchain.llms import Ollama
llm = Ollama(model="llama2")
print(llm("Test query"))

## Design ChatPrompt Template
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context.
Think step by step before providing a detailed answer.
I will tip you $1000 if the user finds the answer helpful.
<context>
{context}
</context>
Question: {input}""")

## Chain Introduction
## Create Stuff Docment Chain

from langchain.chains.combine_documents import create_stuff_documents_chain

document_chain=create_stuff_documents_chain(llm,prompt)

"""
Retrievers: A retriever is an interface that returns documents given
 an unstructured query. It is more general than a vector store.
 A retriever does not need to be able to store documents, only to
 return (or retrieve) them. Vector stores can be used as the backbone
 of a retriever, but there are other types of retrievers as well.
 https://python.langchain.com/docs/modules/data_connection/retrievers/
"""

retriever=db.as_retriever()
retriever

"""
Retrieval chain:This chain takes in a user inquiry, which is then
passed to the retriever to fetch relevant documents. Those documents
(and original inputs) are then passed to an LLM to generate a response
https://python.langchain.com/docs/modules/chains/
"""
from langchain.chains import create_retrieval_chain
retrieval_chain=create_retrieval_chain(retriever,document_chain)

response=retrieval_chain.invoke({"input":"Scaled Dot-Product Attention"})

response['answer']

