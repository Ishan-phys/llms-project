from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import sys

from src.helpers import load_pdf, text_split, download_hugging_face_embeddings
from src.exception import CustomException
from src.logger import logger

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")

def store_index(data_dir, index_name, chunk_size=400, chunk_overlap=20, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Index the data in Pinecone

    Args:
        data_dir (str): path to the directory where the pdf data is stored
        index_name (str): Name of the index
        chunk_size (int): Size of the chunks to split the data into
        chunk_overlap (int): Overlap between the chunks
        model_name (str): Name of the model (for embedding) to download
    """
    try:
        # Extract the data from the PDFs
        extracted_data = load_pdf(data_dir)

        # Split the extracted data into chunks
        text_chunks = text_split(extracted_data, chunk_size, chunk_overlap)

        # Download the Hugging Face embeddings
        embeddings = download_hugging_face_embeddings(model_name)

        # Create the PineconeVectorStore and index the data
        docsearch = PineconeVectorStore.from_documents(text_chunks, embeddings, index_name=index_name)

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

    return docsearch


if __name__ == "__main__":

    index_name = "medical-bot"

    docsearch = store_index(data_dir="data/", index_name=index_name)