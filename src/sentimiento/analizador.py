import os
import requests
import numpy as np

# ── Configuración ──────────────────────────────────────────
MODELO_HF = os.getenv("MODELO_HF", "Cristian022/proyecto-fifa-sentimiento")
HF_TOKEN = os.getenv("HF_TOKEN", "")
API_URL = f"https://api-inference.huggingface.co/models/{MODELO_HF}"
ETIQUETAS = {0: "negativo", 1: "neutral", 2: "positivo"}

def preprocesar_texto(texto):
    """Maneja negaciones comunes en español."""
    negaciones = {
        "no estuvo mal": "estuvo bien",
        "no jugaron mal": "jugaron bien",
        "no fue tan malo": "fue aceptable",
        "no está mal": "está bien",
        "no estuvo tan mal": "estuvo bien",
        "nada mal": "bastante bien",
        "no tan malo": "aceptable"
    }
    texto_lower = texto.lower()
    for negacion, reemplazo in negaciones.items():
        if negacion in texto_lower:
            texto = texto_lower.replace(negacion, reemplazo)
    return texto

class AnalizadorSentimiento:
    def __init__(self):
        print("Iniciando AnalizadorSentimiento via API de HuggingFace...")
        self.headers = {}
        if HF_TOKEN:
            self.headers["Authorization"] = f"Bearer {HF_TOKEN}"
        print("Analizador listo.")

    def analizar(self, texto):
        """Analiza el sentimiento usando la API de HuggingFace."""
        texto = preprocesar_texto(texto)
        
        try:
            respuesta = requests.post(
                API_URL,
                headers=self.headers,
                json={"inputs": texto},
                timeout=30
            )
            
            if respuesta.status_code == 503:
                # Modelo cargando, esperar
                return self._respuesta_error("Modelo cargando, intenta de nuevo en 20 segundos")
            
            resultado = respuesta.json()
            
            if isinstance(resultado, list) and len(resultado) > 0:
                if isinstance(resultado[0], list):
                    scores = resultado[0]
                else:
                    scores = resultado
                
                # Mapear etiquetas del modelo a nuestras etiquetas
                probs = {"negativo": 0.0, "neutral": 0.0, "positivo": 0.0}
                
                for item in scores:
                    label = item.get("label", "").lower()
                    score = item.get("score", 0.0)
                    
                    if "neg" in label or label == "0" or label == "negativo":
                        probs["negativo"] = score
                    elif "neu" in label or label == "1" or label == "neutral":
                        probs["neutral"] = score
                    elif "pos" in label or label == "2" or label == "positivo":
                        probs["positivo"] = score

                # Umbral ajustado para positivos
                UMBRAL_POSITIVO = 0.40
                if probs["positivo"] >= UMBRAL_POSITIVO:
                    prediccion = "positivo"
                elif probs["negativo"] >= probs["neutral"]:
                    prediccion = "negativo"
                else:
                    prediccion = "neutral"

                confianza = probs[prediccion]

                return {
                    "etiqueta": prediccion,
                    "confianza": confianza,
                    "probabilidades": probs
                }
            else:
                return self._respuesta_error("Error en respuesta de API")
                
        except Exception as e:
            print(f"Error en API: {e}")
            return self._respuesta_error(str(e))

    def _respuesta_error(self, mensaje):
        """Retorna respuesta de error estándar."""
        return {
            "etiqueta": "neutral",
            "confianza": 0.0,
            "probabilidades": {
                "negativo": 0.0,
                "neutral": 1.0,
                "positivo": 0.0
            },
            "error": mensaje
        }

    def analizar_lote(self, textos):
        """Analiza múltiples comentarios."""
        resultados = []
        for texto in textos:
            resultado = self.analizar(texto)
            resultado["texto"] = texto
            resultados.append(resultado)
        return resultados