from pathlib import Path

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from source.config import (
    DATA_DIR,
    VECTOR_DB_DIR,
    OPENAI_API_KEY
)


FAISS_INDEX_NAME = "policy_index"


def get_embeddings():

    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY
    )


def load_documents():

    documents = []

    pdf_files = list(
        DATA_DIR.glob("*.pdf")
    )

    if not pdf_files:

        raise ValueError(
            "No PDF files found in data directory."
        )

    for pdf_file in pdf_files:

        loader = PyPDFLoader(
            str(pdf_file)
        )

        documents.extend(
            loader.load()
        )

    return documents


def split_documents():

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(
        docs
    )


def build_vector_store():

    chunks = split_documents()

    vectorstore = FAISS.from_documents(
        chunks,
        get_embeddings()
    )

    VECTOR_DB_DIR.mkdir(
        exist_ok=True
    )

    vectorstore.save_local(
        str(VECTOR_DB_DIR / FAISS_INDEX_NAME)
    )

    return vectorstore


def load_vector_store():

    index_path = VECTOR_DB_DIR / FAISS_INDEX_NAME

    if not index_path.exists():

        return build_vector_store()

    return FAISS.load_local(
        str(index_path),
        get_embeddings(),
        allow_dangerous_deserialization=True
    )


def get_retriever():

    vectorstore = load_vector_store()

    return vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )


def retrieve_context(
    query: str
):

    retriever = get_retriever()

    return retriever.invoke(query)