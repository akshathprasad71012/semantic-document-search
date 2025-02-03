import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("faiss_index.bin")
with open("document_names.pkl", 'rb') as f:
    document_names = pickle.load(f)

querry = input("Enter the querry  : ")
embedding = model.encode([querry], normalize_embeddings=True)
distances, indices = index.search(np.array(embedding, dtype=np.float32), 5)

results = [(document_names[i], distances[0][j]) for j, i in enumerate(indices[0])]
for doc, score in results:
    print(doc, score)
