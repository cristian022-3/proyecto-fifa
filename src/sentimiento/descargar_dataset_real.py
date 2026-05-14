import pandas as pd
from datasets import load_dataset
import os

ARCHIVO_SALIDA = "data/raw/dataset_real.csv"

def descargar_y_procesar():
    print("=" * 50)
    print("DESCARGANDO DATASETS REALES EN ESPAÑOL")
    print("=" * 50)
    
    comentarios = []

    # Dataset 1 — Amazon Reviews en español
    print("\nDescargando Dataset 1: Amazon Reviews español...")
    try:
        dataset1 = load_dataset(
            "mteb/amazon_reviews_multi",
            "es",
            split="train[:3000]",
            trust_remote_code=False
        )
        
        count = 0
        for ejemplo in dataset1:
            texto = ejemplo.get("text", "").strip()
            estrellas = ejemplo.get("label", -1)
            
            if estrellas in [0, 1]:
                etiqueta = "negativo"
            elif estrellas == 2:
                etiqueta = "neutral"
            elif estrellas in [3, 4]:
                etiqueta = "positivo"
            else:
                continue
            
            if texto and len(texto) > 10:
                comentarios.append({
                    "texto": texto[:200],
                    "etiqueta": etiqueta
                })
                count += 1
        
        print(f"Dataset 1: {count} comentarios obtenidos")
    except Exception as e:
        print(f"Dataset 1 error: {e}")

    # Dataset 2 — Spanish Financial News Sentiment
    print("\nDescargando Dataset 2: Sentiment español general...")
    try:
        dataset2 = load_dataset(
            "sst2",
            split="train[:1000]"
        )
        print("Dataset 2: No aplica para español, omitiendo...")
    except Exception as e:
        print(f"Dataset 2 error: {e}")

    # Dataset 3 — Yelp en español adaptado
    print("\nDescargando Dataset 3: Reviews multilingüe...")
    try:
        dataset3 = load_dataset(
            "Helsinki-NLP/opus-100",
            "en-es",
            split="train[:500]",
            trust_remote_code=False
        )
        print("Dataset 3: No aplica directamente, omitiendo...")
    except Exception as e:
        print(f"Dataset 3 error: {e}")

    # Dataset 4 — XNLI español para contexto
    print("\nDescargando Dataset 4: Sentiment analysis español...")
    try:
        dataset4 = load_dataset(
            "dvilares/head_qa",
            "es",
            split="train[:500]",
            trust_remote_code=False
        )
        print("Dataset 4: No aplica directamente, omitiendo...")
    except Exception as e:
        print(f"Dataset 4 error: {e}")

    # Verificar si tenemos datos
    if not comentarios:
        print("\nUsando estrategia alternativa con dataset de HuggingFace...")
        try:
            dataset_alt = load_dataset(
                "sepidmnorozy/Spanish_sentiment",
                split="train"
            )
            
            mapa = {0: "negativo", 1: "positivo"}
            count = 0
            
            for ejemplo in dataset_alt:
                texto = ejemplo.get("text", "").strip()
                etiqueta_num = ejemplo.get("label", -1)
                etiqueta = mapa.get(etiqueta_num, "")
                
                if texto and etiqueta and len(texto) > 5:
                    comentarios.append({
                        "texto": texto[:200],
                        "etiqueta": etiqueta
                    })
                    count += 1
            
            print(f"Dataset alternativo: {count} comentarios")
        except Exception as e:
            print(f"Dataset alternativo error: {e}")

    if not comentarios:
        print("\nNo se encontraron datasets accesibles.")
        print("Continuaremos solo con datos sintéticos.")
        return

    # Guardar
    os.makedirs("data/raw", exist_ok=True)
    df = pd.DataFrame(comentarios)
    df = df.drop_duplicates(subset=["texto"])
    df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")
    
    negativos = len(df[df["etiqueta"] == "negativo"])
    positivos = len(df[df["etiqueta"] == "positivo"])
    neutrales = len(df[df["etiqueta"] == "neutral"])
    
    print("\n" + "=" * 50)
    print("RESULTADO FINAL")
    print(f"Total comentarios reales: {len(df)}")
    print(f"Negativos:  {negativos}")
    print(f"Positivos:  {positivos}")
    print(f"Neutrales:  {neutrales}")
    print(f"Guardado en: {ARCHIVO_SALIDA}")
    print("=" * 50)

if __name__ == "__main__":
    descargar_y_procesar()