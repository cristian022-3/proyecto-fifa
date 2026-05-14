import os
import json
import csv
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CLIENTE_GROQ = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODELO = "llama-3.1-8b-instant"
ARCHIVO_SALIDA = "data/raw/dataset_neutrales.csv"

PROMPT = """Genera exactamente 25 comentarios NEUTRALES realistas de aficionados 
latinoamericanos en Twitter sobre partidos de fútbol del Mundial FIFA 2025-2026.

Comentarios neutrales son observaciones objetivas como:
- Estadísticas del partido
- Descripciones tácticas
- Comparaciones entre equipos
- Datos históricos
- Observaciones sobre jugadores sin carga emocional

Responde ÚNICAMENTE con JSON válido:
[
  {{"texto": "comentario neutral aquí", "etiqueta": "neutral"}}
]"""

def main():
    print("Generando comentarios neutrales adicionales...")
    todos = []
    
    for i in range(1, 41):
        print(f"Lote {i}/40...", end="\r")
        try:
            respuesta = CLIENTE_GROQ.chat.completions.create(
                model=MODELO,
                messages=[{"role": "user", "content": PROMPT}],
                max_tokens=2000,
                temperature=0.7
            )
            
            texto = respuesta.choices[0].message.content.strip()
            if texto.startswith("```"):
                texto = texto.split("```")[1]
                if texto.startswith("json"):
                    texto = texto[4:]
            
            comentarios = json.loads(texto)
            todos.extend(comentarios)
        except Exception as e:
            print(f"Error lote {i}: {e}")
        
        time.sleep(2)
    
    os.makedirs("data/raw", exist_ok=True)
    with open(ARCHIVO_SALIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["texto", "etiqueta"])
        writer.writeheader()
        writer.writerows([
            {"texto": c.get("texto", ""), "etiqueta": "neutral"}
            for c in todos if c.get("texto")
        ])
    
    print(f"\nNeutrales generados: {len(todos)}")
    print(f"Guardado en: {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    main()