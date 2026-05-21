from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ================= LOAD PDF =================
def doc_load(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents


# ================= CHUNKING =================
def chunks_split(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks


# ================= EMBEDDINGS =================
def emb_and_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vectorstore.as_retriever()

    return retriever


# ================= MAIN FUNCTION =================
def main_fun(pdf_path):

    dcmts = doc_load(pdf_path)

    chunks = chunks_split(dcmts)

    retriever = emb_and_store(chunks)

    return retriever