import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Cargar índice y chunks
print("Cargando índice FAISS...")
indice = faiss.read_index("indices/faiss_reglamento.index")
with open("indices/chunks_reglamento.pkl", "rb") as f:
    chunks = pickle.load(f)

# Cargar modelo de embeddings
modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Preguntas de prueba
preguntas = [
    "¿Cuántos cambios puede hacer un equipo en un partido?",
    "¿Puede un portero anotar gol con la mano?",
    "¿Qué es el fuera de juego?",
    "¿Cuánto dura un partido?",
    "¿Cuál es la receta del arroz con leche?"
]

print("\n" + "="*50)
print("PRUEBA DE BÚSQUEDA EN EL REGLAMENTO")
print("="*50)

for pregunta in preguntas:
    print(f"\nPregunta: {pregunta}")
    print("-"*40)
    
    # Generar embedding de la pregunta
    embedding = modelo.encode([pregunta])
    embedding = np.array(embedding).astype("float32")
    
    # Buscar en FAISS
    distancias, indices = indice.search(embedding, k=3)
    
    # Mostrar resultado más relevante
    print("Top 3 fragmentos encontrados:")
    for j in range(3):
        chunk_relevante = chunks[indices[0][j]]
        print(f"\n[Fragmento {j+1}] Distancia: {distancias[0][j]:.4f}")
        print(f"{chunk_relevante[:200]}...")

print("\n" + "="*50)
print("PRUEBA COMPLETADA")
print("="*50)