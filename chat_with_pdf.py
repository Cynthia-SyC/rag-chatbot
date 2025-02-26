import io
import streamlit as st
from openai import OpenAI
from os import environ
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

client = OpenAI(api_key=environ['OPENAI_API_KEY'])

# functions
# load the docs
def load_txt_file(file_bytes: bytes, source_name: str):
    """Load a TXT file."""
    text_content = file_bytes.decode("utf-8", errors="ignore")
    return [Document(page_content=text_content, metadata={"source": source_name})]

def load_pdf_file(file_bytes: bytes, source_name: str):
    """Load a PDF file using pdfplumber."""
    all_text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
    joined_text = "\n".join(all_text)
    return [Document(page_content=joined_text, metadata={"source": source_name})] if joined_text else []

# splitting
def chunk_documents(docs, chunk_size=800, chunk_overlap=100):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)

# retrieval
llm = AzureChatOpenAI(
    azure_endpoint="https://api.ai.it.cornell.edu/",
    deployment_name="gpt-4o",
    temperature=0.2,
    api_version="2023-06-01-preview",
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://api.ai.it.cornell.edu/",
    api_key=environ["OPENAI_API_KEY"],
    model="openai.text-embedding-3-large"
)

st.title("📝 File Q&A with OpenAI")
uploaded_files = st.file_uploader(
    "Upload one or more articles here:",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the uploaded article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if uploaded_files:
    all_docs = []
    for uploaded_file in uploaded_files:
        source_name = uploaded_file.name
        file_bytes = uploaded_file.read()
        if source_name.endswith(".txt"):
            all_docs.extend(load_txt_file(file_bytes, source_name))
        elif source_name.endswith(".pdf"):
            all_docs.extend(load_pdf_file(file_bytes, source_name))
    
    doc_chunks = chunk_documents(all_docs)
    vectorstore = Chroma.from_documents(documents=doc_chunks, embedding=embeddings)

    if question:
        # Read the content of the uploaded file
        # file_content = uploaded_file.read().decode("utf-8")
        # print(file_content)

        # Append the user's question to the messages
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        relevant_docs = vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="openai.gpt-4o",  # Change this to a valid model name
                messages=[
                    {"role": "system", "content": f"Here's the extracted context from the uploaded documents:\n\n{context}"},
                    *st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(stream)

        # Append the assistant's response to the messages
        st.session_state.messages.append({"role": "assistant", "content": response})


