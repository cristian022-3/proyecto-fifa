
import pandas as pd
import os

ARCHIVO_SALIDA = "data/procesado/dataset_final.csv"

def combinar_y_balancear():
    print("=" * 50)
    print("COMBINANDO DATASETS")
    print("=" * 50)
    
    dfs = []
    
    # Dataset 1 — Sintéticos de fútbol
    try:
        df1 = pd.read_csv("data/raw/dataset_sentimiento.csv")
        df1 = df1[["texto", "etiqueta"]]
        df1 = df1[df1["etiqueta"].isin(["positivo", "negativo", "neutral"])]
        print(f"Dataset sintético: {len(df1)} comentarios")
        dfs.append(df1)
    except Exception as e:
        print(f"Error cargando sintético: {e}")
    
    # Dataset 2 — YouTube real
    # Dataset 2 — YouTube real
    try:
        df2 = pd.read_csv("data/raw/dataset_youtube_etiquetado.csv")
        df2 = df2[["texto", "etiqueta"]]
        df2 = df2[df2["etiqueta"].isin(["positivo", "negativo", "neutral"])]
        print(f"Dataset YouTube: {len(df2)} comentarios")
        dfs.append(df2)
    except Exception as e:
        print(f"Error cargando YouTube: {e}")
    
    # Dataset 3 — Neutrales adicionales      ← AGREGAR AQUÍ
    try:
        df3 = pd.read_csv("data/raw/dataset_neutrales.csv")
        df3 = df3[["texto", "etiqueta"]]
        df3 = df3[df3["etiqueta"].isin(["positivo", "negativo", "neutral"])]
        print(f"Dataset neutrales adicionales: {len(df3)} comentarios")
        dfs.append(df3)
    except Exception as e:
        print(f"Error cargando neutrales: {e}")
    
    # Combinar todos                         ← ESTA LÍNEA YA EXISTE
    df_total = pd.concat(dfs, ignore_index=True)
    
    # Combinar todos
    df_total = pd.concat(dfs, ignore_index=True)
    df_total = df_total.drop_duplicates(subset=["texto"])
    df_total = df_total.dropna()
    
    print(f"\nTotal antes de balancear: {len(df_total)}")
    
    # Mostrar distribución actual
    print("\nDistribución actual:")
    print(df_total["etiqueta"].value_counts())
    
    # Balancear clases
    min_clase = df_total["etiqueta"].value_counts().min()
    limite_por_clase = min(min_clase, 1200)
    
    df_balanceado = pd.concat([
        df_total[df_total["etiqueta"] == "positivo"].sample(
            n=limite_por_clase, random_state=42
        ),
        df_total[df_total["etiqueta"] == "negativo"].sample(
            n=limite_por_clase, random_state=42
        ),
        df_total[df_total["etiqueta"] == "neutral"].sample(
            n=limite_por_clase, random_state=42
        )
    ]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Dividir 70/15/15
    n = len(df_balanceado)
    n_train = int(n * 0.70)
    n_val = int(n * 0.15)
    
    df_train = df_balanceado[:n_train]
    df_val = df_balanceado[n_train:n_train + n_val]
    df_test = df_balanceado[n_train + n_val:]
    
    # Guardar
    os.makedirs("data/procesado", exist_ok=True)
    df_balanceado.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")
    df_train.to_csv("data/procesado/train.csv", index=False, encoding="utf-8")
    df_val.to_csv("data/procesado/val.csv", index=False, encoding="utf-8")
    df_test.to_csv("data/procesado/test.csv", index=False, encoding="utf-8")
    
    print("\nDistribución final balanceada:")
    print(df_balanceado["etiqueta"].value_counts())
    
    print("\n" + "=" * 50)
    print("DATASET FINAL LISTO")
    print(f"Total balanceado: {len(df_balanceado)}")
    print(f"Entrenamiento (70%): {len(df_train)}")
    print(f"Validación (15%):    {len(df_val)}")
    print(f"Prueba (15%):        {len(df_test)}")
    print(f"Guardado en: {ARCHIVO_SALIDA}")
    print("=" * 50)

if __name__ == "__main__":
    combinar_y_balancear()