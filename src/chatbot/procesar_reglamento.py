import os
import pickle
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# ── Configuración ──────────────────────────────────────────
PDF_PATH = "data/raw/reglamento_fifa.pdf"
INDICE_PATH = "indices/faiss_reglamento.index"
CHUNKS_PATH = "indices/chunks_reglamento.pkl"
MODELO_EMBEDDINGS = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

def limpiar_texto(texto):
    """Limpia caracteres extraños del PDF."""
    import re
    # Eliminar caracteres no imprimibles
    texto = re.sub(r'[^\x20-\x7E\xC0-\xFF\u00C0-\u024F\n]', ' ', texto)
    # Corregir solo consonantes duplicadas que no son válidas en español
    # (no tocar ll, rr, cc, que son válidas)
    pares_invalidos = ['bb','dd','ff','gg','hh','jj','kk','mm',
                       'nn','pp','qq','ss','tt','vv','ww','xx',
                       'yy','zz','aa','ee','ii','oo','uu']
    for par in pares_invalidos:
        texto = re.sub(par, par[0], texto)
    # Eliminar múltiples espacios
    texto = re.sub(r' +', ' ', texto)
    # Eliminar múltiples saltos de línea
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    # Eliminar líneas muy cortas
    lineas = texto.split('\n')
    lineas_limpias = [l for l in lineas if len(l.strip()) > 10]
    return '\n'.join(lineas_limpias)
def es_chunk_valido(chunk):
    """Verifica que el chunk no tenga texto corrupto."""
    import re
    # Detectar patrones de texto corrupto
    # Letras mezcladas con mayúsculas en medio de palabra
    patron_corrupto = re.compile(r'[a-z][A-Z][a-z]')
    # Palabras con consonantes triplicadas
    patron_triple = re.compile(r'([bcdfghjklmnpqrstvwxyz])\1\1')
    # Espacios dentro de palabras normales
    patron_espacios = re.compile(r'\b\w\s\w\s\w\b')
    
    if patron_corrupto.search(chunk):
        return False
    if patron_triple.search(chunk):
        return False
    if len(re.findall(r'[A-Z]', chunk)) > len(chunk) * 0.15:
        return False
    return True

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto limpio del PDF usando pdfplumber."""
    print(f"Leyendo PDF: {ruta_pdf}")
    texto_completo = ""
    
    with pdfplumber.open(ruta_pdf) as pdf:
        total_paginas = len(pdf.pages)
        for i, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
            print(f"  Página {i+1}/{total_paginas} procesada", end="\r")
    
    texto_limpio = limpiar_texto(texto_completo)
    print(f"\nTexto extraído: {len(texto_limpio)} caracteres")
    return texto_limpio

def crear_chunks(texto, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Divide el texto en chunks con solapamiento."""
    palabras = texto.split()
    chunks = []
    inicio = 0
    
    while inicio < len(palabras):
        fin = inicio + chunk_size
        chunk = " ".join(palabras[inicio:fin])
        if len(chunk.strip()) > 50 and es_chunk_valido(chunk):
            chunks.append(chunk)
        inicio += chunk_size - overlap
    
    print(f"Chunks creados: {len(chunks)}")
    return chunks

def construir_indice_faiss(chunks, modelo_nombre=MODELO_EMBEDDINGS):
    """Genera embeddings y construye el índice FAISS."""
    print(f"Cargando modelo de embeddings: {modelo_nombre}")
    modelo = SentenceTransformer(modelo_nombre)
    
    print("Generando embeddings para cada chunk...")
    embeddings = modelo.encode(
        chunks,
        show_progress_bar=True,
        batch_size=32
    )
    
    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]
    
    print(f"Dimensión de embeddings: {dimension}")
    print("Construyendo índice FAISS...")
    
    indice = faiss.IndexFlatL2(dimension)
    indice.add(embeddings)
    
    print(f"Índice construido con {indice.ntotal} vectores")
    return indice

def guardar_resultados(indice, chunks):
    """Guarda el índice FAISS y los chunks en disco."""
    os.makedirs("indices", exist_ok=True)
    faiss.write_index(indice, INDICE_PATH)
    print(f"Índice guardado en: {INDICE_PATH}")
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Chunks guardados en: {CHUNKS_PATH}")

def main():
    print("=" * 50)
    print("PROCESANDO REGLAMENTO FIFA (versión mejorada)")
    print("=" * 50)
    
    texto = extraer_texto_pdf(PDF_PATH)
    chunks = crear_chunks(texto)
    indice = construir_indice_faiss(chunks)
    guardar_resultados(indice, chunks)
    
    print("=" * 50)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print(f"Total chunks indexados: {len(chunks)}")
    print("=" * 50)

if __name__ == "__main__":
    main()