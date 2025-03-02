from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")
index = faiss.read_index("faiss_index.bin")
with open("document_names.pkl", 'rb') as f:
    document_names = pickle.load(f)

app = FastAPI()
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{querry}/{number}")
async def root(querry: str, number: int = 5):
    embedding = model.encode([querry], normalize_embeddings=True)
    distances, indices = index.search(np.array(embedding, dtype=np.float32), max(1, number))
    return_val = []
    results = [(document_names[i], distances[0][j]) for j, i in enumerate(indices[0])]
    for doc, score in results:
        return_val.append(doc)
    return {"results": return_val}
