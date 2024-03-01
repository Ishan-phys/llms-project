from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf(data_dir):
    """Load PDFs from a directory

    Args:
        data_dir (str): path to the directory where the pdf data is stored

    Returns:
        _type_: _description_
    """
    loader = DirectoryLoader(data_dir,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    documents = loader.load()

    return documents

def text_split(extracted_data, chunk_size=500, chunk_overlap=20):
    """Split the extracted data into chunks

    Args:
        extracted_data (_type_): _description_

    Returns:
        _type_: _description_
    """

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.split_documents(extracted_data)

    return documents


def download_hugging_face_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Download the Hugging Face embeddings

    Args:
        model_name (str): Name of the model to download

    Returns:
        _type_: _description_
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    return embeddings