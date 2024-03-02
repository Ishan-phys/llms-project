# Medical ChatBot using Llama2 - Answers you medical related query

## Steps to run the project 


### Step 1: Clone the repository

```bash
git clone https://github.com/Ishan-phys/llms-project.git
```

### Setp 2: Install the required packages and setup the virtual environment

```bash
venv -p python3.10 venv
```

```bash
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

### Create a .env file and add the following variables

```ini
HUGGINGFACEHUB_API_TOKEN=xxxxxxxxxxxxxxxx
PINECONE_API_KEY=xxxxxxxxxxxxxxxx
PINECONE_API_ENV=xxxxxxxxxxxxxxxx
```

### Download the quantized model from the Hugging Face Model hub and save it in the models directory


```ini 
## Download the Llama 2 Model:
llama-2-7b-chat.ggmlv3.q4_0.bin

## From the following link
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
```

### Set the document store and the retriever in the data folder

```ini

## Set the document store and the retriever in the data folder
document_store = "data/documment.pdf"

## Setup the Pinecone Index on the Pinecone Console
https://www.pinecone.io/
```

### Store the index in the pinecone database

```bash
python3 store_index.py
```

### Run the application

```bash
python3 app.py
```

### Interact with the chatbot
 
Open the following link in the browser

```bash
http://127.0.0.0:8080
```

Type in the medical related query and the chatbot will answer the query

