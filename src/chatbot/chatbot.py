import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ── Configuración ──────────────────────────────────────────
INDICE_PATH = "indices/faiss_reglamento.index"
CHUNKS_PATH = "indices/chunks_reglamento.pkl"
MODELO_EMBEDDINGS = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODELO_LLM = "llama-3.1-8b-instant"
TOP_K = 3

# ── Preguntas frecuentes precargadas (caché instantánea) ───
CACHE_PREGUNTAS = {
    "cuanto dura un partido": "Un partido de fútbol se divide en dos periodos iguales de 45 minutos cada uno, con una pausa de medio tiempo no superior a 15 minutos. El árbitro puede añadir tiempo de descuento al final de cada periodo. En caso de empate en competiciones eliminatorias, se pueden disputar dos periodos extra de máximo 15 minutos cada uno. (Regla 7 — Duración del partido)",
    "cuantos jugadores tiene un equipo": "Cada equipo está formado por un máximo de 11 jugadores, incluido el guardameta. Un partido no puede comenzar ni continuar si un equipo tiene menos de 7 jugadores. (Regla 3 — El número de jugadores)",
    "que es el fuera de juego": "Un jugador está en posición de fuera de juego si cualquier parte de su cabeza, cuerpo o pies está en la mitad del campo contraria y más cerca de la línea de gol que el balón y el penúltimo defensor. No se puede estar en fuera de juego en el propio campo. (Regla 11 — El fuera de juego)",
    "cuando es penal": "Se concede un tiro penal cuando un jugador comete una infracción sancionable con tiro libre directo dentro de su propia área penal. (Regla 12 — Faltas e incorrecciones)",
    "que es tarjeta roja": "La tarjeta roja significa expulsión del jugador. Se muestra por conducta violenta, escupir, morder, lenguaje ofensivo, dos amonestaciones en el mismo partido, o impedir un gol mediante mano o falta. (Regla 12 — Faltas e incorrecciones)",
    "que es tarjeta amarilla": "La tarjeta amarilla es una amonestación. Se muestra por conducta antideportiva, protestar, retrasar el juego, no respetar la distancia en faltas, entrar o salir sin permiso, o infringir las reglas repetidamente. (Regla 12 — Faltas e incorrecciones)",
    "como se cobra un tiro libre": "En un tiro libre directo el ejecutor puede marcar gol directamente. En un tiro libre indirecto el balón debe tocar a otro jugador antes de entrar. El balón debe estar estático y los adversarios a 9.15 metros. (Regla 13 — Tiros libres)",
    "que es el var": "El VAR es el árbitro asistente de vídeo. Revisa situaciones relacionadas con goles, penales, tarjetas rojas directas y confusiones de identidad, interviniendo solo ante errores claros y manifiestos. (Regla 5 — El árbitro)",
    "cuanto mide el campo": "El campo de juego debe ser rectangular. La longitud de la línea de banda debe estar entre 90 y 120 metros, y la longitud de la línea de meta entre 45 y 90 metros. (Regla 1 — El terreno de juego)",
    "que pasa si el balon sale": "Si el balón sale completamente por la línea de banda se reanuda con un saque de banda. Si sale por la línea de meta se reanuda con saque de esquina o saque de meta según quién lo tocó último. (Reglas 15, 16 y 17)",
}

def normalizar_pregunta(pregunta):
    """Normaliza la pregunta para buscar en caché."""
    pregunta = pregunta.lower().strip()
    pregunta = pregunta.replace("¿", "").replace("?", "")
    pregunta = pregunta.replace("á", "a").replace("é", "e")
    pregunta = pregunta.replace("í", "i").replace("ó", "o")
    pregunta = pregunta.replace("ú", "u").replace("ü", "u")
    return pregunta

def buscar_en_cache(pregunta):
    """Busca una respuesta instantánea en el caché."""
    pregunta_norm = normalizar_pregunta(pregunta)
    for clave, respuesta in CACHE_PREGUNTAS.items():
        if clave in pregunta_norm or any(
            palabra in pregunta_norm 
            for palabra in clave.split() 
            if len(palabra) > 4
        ):
            return respuesta
    return None

class ChatbotFIFA:
    def __init__(self):
        print("Iniciando ChatbotFIFA...")
        self.modelo_embeddings = SentenceTransformer(MODELO_EMBEDDINGS)
        self.indice = faiss.read_index(INDICE_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            self.chunks = pickle.load(f)
        self.cliente_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.historial = []
        print("Chatbot listo.")

    def buscar_contexto(self, pregunta):
        """Busca los chunks más relevantes en FAISS."""
        embedding = self.modelo_embeddings.encode([pregunta])
        embedding = np.array(embedding).astype("float32")
        distancias, indices = self.indice.search(embedding, k=TOP_K)
        
        chunks_relevantes = []
        for i in range(TOP_K):
            chunks_relevantes.append(self.chunks[indices[0][i]])
        
        return "\n\n---\n\n".join(chunks_relevantes)

    def construir_prompt(self, pregunta, contexto):
        """Construye el prompt con contexto del reglamento."""
        return f"""Eres un asistente experto en el reglamento oficial de fútbol FIFA/IFAB.
Tu única función es responder preguntas sobre las Reglas de Juego basándote 
EXCLUSIVAMENTE en el siguiente contexto extraído del reglamento oficial.

CONTEXTO DEL REGLAMENTO:
{contexto}

INSTRUCCIONES:
- Responde SOLO con información del contexto proporcionado
- Si la pregunta no está relacionada con el reglamento de fútbol, responde: 
  "Solo puedo responder preguntas sobre el reglamento FIFA."
- Si la información no está en el contexto, responde:
  "No encontré información específica sobre eso en el reglamento."
- Responde siempre en español
- Sé claro, preciso y conciso
- Menciona la regla correspondiente cuando sea posible

PREGUNTA: {pregunta}

RESPUESTA:"""

    def responder_stream(self, pregunta):
        """Genera respuesta con streaming. Retorna generador."""
        # Primero verificar caché
        respuesta_cache = buscar_en_cache(pregunta)
        if respuesta_cache:
            yield respuesta_cache
            return

        # Si no está en caché, usar RAG + Groq
        contexto = self.buscar_contexto(pregunta)
        prompt = self.construir_prompt(pregunta, contexto)

        # Llamada a Groq con streaming
        stream = self.cliente_groq.chat.completions.create(
            model=MODELO_LLM,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def obtener_contexto_usado(self, pregunta):
        """Retorna el contexto usado para transparencia."""
        respuesta_cache = buscar_en_cache(pregunta)
        if respuesta_cache:
            return "Respuesta desde caché de preguntas frecuentes."
        contexto = self.buscar_contexto(pregunta)
        return contexto[:500] + "..."