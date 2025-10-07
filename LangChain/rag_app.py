import streamlit as st
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

st.set_page_config(page_title="Local RAG: LangChain + Ollama", layout="wide")
st.title("Local RAG: LangChain + Ollama + Streamlit")

# --- Sidebar: Document Upload ---
st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload text files", type=["txt"], accept_multiple_files=True)

# --- Load and Split Documents ---
documents = []
if uploaded_files:
    for file in uploaded_files:
        text = file.read().decode("utf-8")
        documents.append(Document(page_content=text, metadata={"filename": file.name}))

    # Split into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)
else:
    docs = []

# --- Embedding & Vector Store ---
if docs:
    st.sidebar.success(f"Loaded {len(docs)} chunks from {len(uploaded_files)} files.")
    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()
else:
    retriever = None

# --- Ollama LLM ---
llm = Ollama(model="llama3")

# --- RAG Chain ---
if retriever:
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
else:
    qa_chain = None

# --- Main UI: Ask Questions ---
st.header("Ask a Question About Your Documents")
question = st.text_input("Enter your question:")


if st.button("Get Answer", key="get_answer_btn") and qa_chain and question:
    with st.spinner("Thinking..."):
        answer = qa_chain.run(question)
    st.subheader("Answer:")
    st.write(answer)
elif not retriever and st.button("Get Answer", key="get_answer_warn_btn"):
    st.warning("Please upload documents first.")

st.markdown("---")
st.markdown("Built with [LangChain](https://python.langchain.com/), [Ollama](https://ollama.com/), and [Streamlit](https://streamlit.io/)")
