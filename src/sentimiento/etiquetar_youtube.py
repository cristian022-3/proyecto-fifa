
import os
import csv
import time
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CLIENTE_GROQ = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODELO = "llama-3.1-8b-instant"
ARCHIVO_ENTRADA = "data/raw/dataset_youtube.csv"
ARCHIVO_SALIDA = "data/raw/dataset_youtube_etiquetado.csv"
LOTE_SIZE = 10

PROMPT_ETIQUETADO = """Analiza el sentimiento de estos comentarios de aficionados 
latinoamericanos sobre fútbol. Clasifica cada uno como:
- "positivo": celebración, alegría, elogio, admiración
- "negativo": enojo, tristeza, crítica, insulto, queja
- "neutral": observación objetiva, estadística, descripción

Comentarios a clasificar:
{comentarios}

Responde ÚNICAMENTE con JSON válido sin texto adicional:
[
  {{"id": 0, "etiqueta": "positivo"}},
  {{"id": 1, "etiqueta": "negativo"}}
]"""

def etiquetar_lote(comentarios_lote):
    """Etiqueta un lote de comentarios."""
    texto_comentarios = "\n".join([
        f"{i}. {c['texto'][:150]}" 
        for i, c in enumerate(comentarios_lote)
    ])
    
    prompt = PROMPT_ETIQUETADO.format(comentarios=texto_comentarios)
    
    try:
        respuesta = CLIENTE_GROQ.chat.completions.create(
            model=MODELO,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1
        )
        
        import json
        texto = respuesta.choices[0].message.content.strip()
        
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
        
        etiquetas = json.loads(texto)
        return {e["id"]: e["etiqueta"] for e in etiquetas}
        
    except Exception as e:
        print(f"Error etiquetando lote: {e}")
        return {}

def main():
    print("=" * 50)
    print("ETIQUETANDO COMENTARIOS DE YOUTUBE")
    print("=" * 50)
    
    df = pd.read_csv(ARCHIVO_ENTRADA)
    print(f"Total comentarios a etiquetar: {len(df)}")
    
    # Limitar a 3000 para no saturar Groq
    df = df.head(3000)
    comentarios = df.to_dict("records")
    
    resultados = []
    total_lotes = len(comentarios) // LOTE_SIZE + 1
    errores = 0
    
    for i in range(0, len(comentarios), LOTE_SIZE):
        lote = comentarios[i:i + LOTE_SIZE]
        lote_num = i // LOTE_SIZE + 1
        
        print(f"Etiquetando lote {lote_num}/{total_lotes}...", end="\r")
        
        etiquetas = etiquetar_lote(lote)
        
        for j, comentario in enumerate(lote):
            etiqueta = etiquetas.get(j, "")
            if etiqueta in ["positivo", "negativo", "neutral"]:
                resultados.append({
                    "texto": comentario["texto"],
                    "etiqueta": etiqueta
                })
            else:
                errores += 1
        
        time.sleep(2)
        
        # Guardar cada 100 lotes
        if lote_num % 100 == 0:
            df_parcial = pd.DataFrame(resultados)
            df_parcial.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")
            print(f"\nGuardado parcial: {len(resultados)} comentarios")
    
    # Guardar final
    df_final = pd.DataFrame(resultados)
    df_final.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")
    
    negativos = len(df_final[df_final["etiqueta"] == "negativo"])
    positivos = len(df_final[df_final["etiqueta"] == "positivo"])
    neutrales = len(df_final[df_final["etiqueta"] == "neutral"])
    
    print("\n" + "=" * 50)
    print("ETIQUETADO COMPLETADO")
    print(f"Total etiquetados: {len(df_final)}")
    print(f"Positivos:  {positivos}")
    print(f"Negativos:  {negativos}")
    print(f"Neutrales:  {neutrales}")
    print(f"Errores:    {errores}")
    print(f"Guardado en: {ARCHIVO_SALIDA}")
    print("=" * 50)

if __name__ == "__main__":
    main()