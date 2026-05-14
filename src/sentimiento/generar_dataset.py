import os
import json
import csv
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Configuración ──────────────────────────────────────────
CLIENTE_GROQ = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODELO = "llama-3.1-8b-instant"
ARCHIVO_SALIDA = "data/raw/dataset_sentimiento.csv"
COMENTARIOS_POR_LOTE = 20
TOTAL_LOTES = 50

PROMPT_TEMPLATE = """Genera exactamente {n} comentarios realistas de aficionados 
latinoamericanos en Twitter sobre partidos de fútbol del Mundial FIFA.
Distribuye así:
- {neg} comentarios negativos (usa jerga como: robo, árbitro vendido, 
  vergüenza, desastre, eliminados, fracaso, horrible, injusto)
- {pos} comentarios positivos (usa jerga como: golazo, partidazo, crack, 
  tremendo, campeones, increíble, histórico, brillante)
- {neu} comentarios neutrales (observaciones tácticas, estadísticas, 
  descripciones objetivas del partido)

IMPORTANTE:
- Incluye menciones a jugadores, equipos latinoamericanos y europeos
- Usa lenguaje informal de redes sociales, emojis ocasionales
- Varía la longitud entre 10 y 50 palabras
- Responde ÚNICAMENTE con JSON válido, sin texto adicional
- Formato exacto:
[
  {{"texto": "comentario aquí", "etiqueta": "negativo"}},
  {{"texto": "comentario aquí", "etiqueta": "positivo"}},
  {{"texto": "comentario aquí", "etiqueta": "neutral"}}
]"""

def generar_lote(lote_num):
    """Genera un lote de comentarios usando Groq."""
    prompt = PROMPT_TEMPLATE.format(
        n=COMENTARIOS_POR_LOTE,
        neg=7,
        pos=7,
        neu=6
    )
    
    try:
        respuesta = CLIENTE_GROQ.chat.completions.create(
            model=MODELO,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.8
        )
        
        texto = respuesta.choices[0].message.content.strip()
        
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
        
        comentarios = json.loads(texto)
        print(f"  Lote {lote_num}: {len(comentarios)} comentarios generados")
        return comentarios
        
    except json.JSONDecodeError as e:
        print(f"  Lote {lote_num}: Error JSON - {e}")
        return []
    except Exception as e:
        print(f"  Lote {lote_num}: Error - {e}")
        return []

def normalizar_y_guardar(todos_comentarios):
    """Normaliza campos y guarda el dataset en CSV."""
    os.makedirs("data/raw", exist_ok=True)
    
    comentarios_limpios = []
    for c in todos_comentarios:
        texto = c.get("texto") or c.get("textarea") or c.get("text") or ""
        etiqueta = c.get("etiqueta") or c.get("label") or c.get("sentimiento") or ""
        etiqueta = etiqueta.lower().strip()
        
        if etiqueta not in ["positivo", "negativo", "neutral"]:
            continue
        if texto and etiqueta:
            comentarios_limpios.append({
                "texto": texto.strip(),
                "etiqueta": etiqueta
            })
    
    with open(ARCHIVO_SALIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["texto", "etiqueta"])
        writer.writeheader()
        writer.writerows(comentarios_limpios)
    
    print(f"Dataset guardado: {len(comentarios_limpios)} comentarios en {ARCHIVO_SALIDA}")
    return comentarios_limpios

def main():
    print("=" * 50)
    print("GENERANDO DATASET DE SENTIMIENTO")
    print("=" * 50)
    
    todos_comentarios = []
    errores = 0
    
    for i in range(1, TOTAL_LOTES + 1):
        print(f"Procesando lote {i}/{TOTAL_LOTES}...")
        comentarios = generar_lote(i)
        
        if comentarios:
            todos_comentarios.extend(comentarios)
        else:
            errores += 1
        
        time.sleep(2)
        
        if i % 10 == 0:
            limpios = normalizar_y_guardar(todos_comentarios)
            print(f"Guardado parcial: {len(limpios)} comentarios válidos")
    
    comentarios_finales = normalizar_y_guardar(todos_comentarios)
    
    negativos = sum(1 for c in comentarios_finales if c["etiqueta"] == "negativo")
    positivos = sum(1 for c in comentarios_finales if c["etiqueta"] == "positivo")
    neutrales = sum(1 for c in comentarios_finales if c["etiqueta"] == "neutral")
    
    print("\n" + "=" * 50)
    print("DATASET GENERADO EXITOSAMENTE")
    print(f"Total comentarios válidos: {len(comentarios_finales)}")
    print(f"Negativos:  {negativos}")
    print(f"Positivos:  {positivos}")
    print(f"Neutrales:  {neutrales}")
    print(f"Lotes con error: {errores}")
    print("=" * 50)

if __name__ == "__main__":
    main()