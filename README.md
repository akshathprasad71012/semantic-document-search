# Semantic Document Search

![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

Semantic Document Search allows users to search documents based on their contents.


## How semantic search works?

It uses [Sentence Transformer: A Pretrained Offline Text Encoding Model](https://github.com/UKPLab/sentence-transformers) to convert english text to vector embeddings. These embeddings are stored in a [FAISS Index](https://github.com/facebookresearch/faiss) for fast and efficient similarity search.   

*All the processing, storage and search happens locally on the machine, so once the models are downloaded, internet connection is not needed.*

## Installation

### Backend

The backend consists of a build_index.py file, which goes through all the documents in the selected directory and adds them to FAISS Index.

Once this is done, you can launch the FastAPI backend which uses the Index to respond to queries. 

**NOTE: For FastAPI backend to work, the FAISS Index should be created first by running build_index.py**

```
# Edit the path to the directory containing documents in build_index.py

python build_index.py
uvicorn backend:app
```
You can also search without using the frontend by running search.py script

### Frontend

The frontend is a very minimal search page made using Vite + React. It asks user for document description and makes a get request to FastAPI server.

```
cd frontend/semantic-document-search
npm install
npm run dev
```


