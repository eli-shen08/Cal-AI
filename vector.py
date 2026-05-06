from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
# from chunking_evaluation.chunking import ClusterSemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import os

embed_model = OllamaEmbeddings(model='nomic-embed-text')

vec_db_loc = './vector_database'

vectorize = not os.path.exists(vec_db_loc)

if vectorize:

    # Reading the PDF files
    dir_path = "E:\RAG\Vanilla RAG\V3\Data"
    # loader = PDFPlumberLoader("test.pdf")
    loader = PyPDFDirectoryLoader(dir_path)
    docs = loader.load()

    """
    One of the problems seen with PyPDFLoader is that
    it parses the text as it is with all \n
    so we need to clean the text
    """

    # Cleaning the text 
    cleaned_docs = []
    for doc in docs:
        cleaned_text = " ".join(doc.page_content.split())
        cleaned_docs.append(Document(
            page_content=cleaned_text,
            metadata = doc.metadata
        ))



    """
    For this Rag we are using both Recursive text splitter 
    as well as Semantic Chunking since mxbai-embed-large
    embedding model has a context imit of 512 tokens and the
    sematic chunks are larger than that.
    
    """

    # First using Recursive Chunking to match context size of Embed Model
    # Splitting the output of Recursive Chunking into semantic chunks
    print("Now using Semantic Chunker")
    text_splitter = SemanticChunker(embed_model)
    sem_documents = text_splitter.split_documents(cleaned_docs)
    print("Number of chunks created: ", len(sem_documents))


    print("Now using Recursive text Splitter")
    size_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,      
    chunk_overlap=50    
    )
    rec_documents = size_splitter.split_documents(sem_documents)
    print("Number of Chunks created : ", len(rec_documents))

    vector_store = Chroma.from_documents(
        documents=rec_documents,
        embedding=embed_model,
        persist_directory=vec_db_loc
    )
else:
    vector_store = Chroma(
        persist_directory=vec_db_loc,
        embedding_function=embed_model,
        collection_metadata={"hnsw:space": "cosine"}
    )

retriever = vector_store.as_retriever(
    search_kwargs={"k":7}
)