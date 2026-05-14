import os
import csv
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# ── Configuración ──────────────────────────────────────────
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
ARCHIVO_SALIDA = "data/raw/dataset_youtube.csv"

# Videos de partidos del Mundial FIFA en español
BUSQUEDAS = [
    "Mundial de Clubes FIFA 2025 goles reacciones",
    "Colombia eliminatorias 2026 partido reacciones",
    "Argentina eliminatorias Mundial 2026",
    "Brasil eliminatorias 2026 goles",
    "Copa América 2024 goles mejores momentos",
    "Champions League 2025 final reacciones",
    "Colombia vs Venezuela eliminatorias 2025",
    "Real Madrid Champions 2025 comentarios aficionados",
    "goles Champions League 2024 2025 español",
    "selección Colombia 2025 partido reacciones"
]

def buscar_videos(youtube, query, max_resultados=5):
    """Busca videos relacionados con fútbol."""
    try:
        respuesta = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_resultados,
            type="video",
            relevanceLanguage="es",
            order="relevance"
        ).execute()
        
        videos = []
        for item in respuesta.get("items", []):
            video_id = item["id"]["videoId"]
            titulo = item["snippet"]["title"]
            videos.append({"id": video_id, "titulo": titulo})
        
        return videos
    except Exception as e:
        print(f"Error buscando videos: {e}")
        return []

def obtener_comentarios(youtube, video_id, titulo, max_comentarios=100):
    """Obtiene comentarios de un video."""
    comentarios = []
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            order="relevance"
        )
        
        count = 0
        while request and count < max_comentarios:
            respuesta = request.execute()
            
            for item in respuesta.get("items", []):
                comentario = item["snippet"]["topLevelComment"]["snippet"]
                texto = comentario["textDisplay"].strip()
                likes = comentario["likeCount"]
                
                # Filtrar comentarios muy cortos o muy largos
                if 10 < len(texto) < 300:
                    comentarios.append({
                        "texto": texto,
                        "likes": likes,
                        "video": titulo[:50]
                    })
                    count += 1
            
            # Siguiente página
            if "nextPageToken" in respuesta and count < max_comentarios:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=respuesta["nextPageToken"],
                    textFormat="plainText",
                    order="relevance"
                )
            else:
                break
                
    except Exception as e:
        print(f"  Error en video {video_id}: {e}")
    
    return comentarios

def main():
    print("=" * 50)
    print("RECOLECTANDO COMENTARIOS DE YOUTUBE")
    print("=" * 50)
    
    if not YOUTUBE_API_KEY:
        print("ERROR: YOUTUBE_API_KEY no encontrada en .env")
        return
    
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    todos_comentarios = []
    videos_procesados = set()
    
    for busqueda in BUSQUEDAS:
        print(f"\nBuscando: '{busqueda}'")
        videos = buscar_videos(youtube, busqueda)
        print(f"Videos encontrados: {len(videos)}")
        
        for video in videos:
            if video["id"] in videos_procesados:
                continue
                
            videos_procesados.add(video["id"])
            print(f"  Procesando: {video['titulo'][:60]}...")
            
            comentarios = obtener_comentarios(
                youtube, 
                video["id"], 
                video["titulo"]
            )
            
            todos_comentarios.extend(comentarios)
            print(f"  Comentarios recolectados: {len(comentarios)}")
            
            time.sleep(1)
        
        time.sleep(2)
    
    # Eliminar duplicados
    textos_vistos = set()
    comentarios_unicos = []
    for c in todos_comentarios:
        if c["texto"] not in textos_vistos:
            textos_vistos.add(c["texto"])
            comentarios_unicos.append(c)
    
    # Guardar sin etiqueta (se etiquetarán después)
    os.makedirs("data/raw", exist_ok=True)
    with open(ARCHIVO_SALIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["texto", "likes", "video"])
        writer.writeheader()
        writer.writerows(comentarios_unicos)
    
    print("\n" + "=" * 50)
    print("RECOLECCIÓN COMPLETADA")
    print(f"Total comentarios únicos: {len(comentarios_unicos)}")
    print(f"Videos procesados: {len(videos_procesados)}")
    print(f"Guardado en: {ARCHIVO_SALIDA}")
    print("=" * 50)

if __name__ == "__main__":
    main()