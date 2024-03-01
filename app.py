from flask import Flask, request, jsonify, render_template
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
import sys

from src.prompt import *
from src.helpers import download_hugging_face_embeddings
from src.logger import logger
from src.exception import CustomException

load_dotenv()

app = Flask(__name__)


def get_embedding():
    """Get the embedding

    Returns:
        _type_: _description_
    """
    try:
        embedding = download_hugging_face_embeddings()

        logger.info("Embedding loaded successfully")

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)
    
    return embedding

def initialize_vector_store(embedding, index_name="medical-bot"):
    """Initialize the vector store

    Args:
        embedding (_type_): _description_
        index_name (str): Name of the index

    Returns:
        docsearch object
    """
    try:
        docsearch = PineconeVectorStore(index_name=index_name, embedding=embedding)

        logger.info(f"Index {index_name} loaded successfully")

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

    return docsearch

def initialize_llm(model_dir="model/llama-2-7b-chat.ggmlv3.q4_0.bin", model_type="llama", max_tokens=512, temperature=0.8):
    """Initialize the LLM

    Args:
        model_dir (str): Path to the model directory
        model_type (str): Type of the model
        max_tokens (int): Maximum number of tokens
        temperature (float): Temperature

    Returns:
        _type_: _description_
    """
    try:
        llm = CTransformers(
                model=model_dir,
                model_type=model_type, 
                config={'max_new_tokens':max_tokens,
                        'temperature':temperature
            })
        
        logger.info("LLM loaded successfully")

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

    return llm

def initialize_rag_chain(llm, docsearch, prompt):
    """Initialize the RAG chain

    Args:
        llm (_type_): _description_
        docsearch (_type_): _description_
        prompt (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        rag_chain = (
            {"context": docsearch.as_retriever(search_kwargs={'k':2}), "question": RunnablePassthrough()}
            | prompt
            | llm 
            | StrOutputParser()
        )

        logger.info("RAG chain loaded successfully")

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

    return rag_chain

llm       = initialize_llm()
embedding = get_embedding()
docsearch = initialize_vector_store(embedding, index_name="medical-bot")
prompt    = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
rag_chain = initialize_rag_chain(llm, docsearch, prompt)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/get', methods=['GET', 'POST'])
def chat():

    msg = request.form['msg']
    input = msg

    print("input", input)

    output = rag_chain.invoke(input)

    print(f"LLM Output: {output}")

    return str(output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)