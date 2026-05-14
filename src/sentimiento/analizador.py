import os
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ── Configuración ──────────────────────────────────────────
MODELO_PATH = os.getenv("MODELO_HF", "Cristian022/proyecto-fifa-sentimiento")
ETIQUETAS = {0: "negativo", 1: "neutral", 2: "positivo"}
MAX_LENGTH = 128

# Palabras claramente positivas en contexto futbolístico
PALABRAS_POSITIVAS = [
    "golazo", "campeones", "campeon", "ganamos", "ganaron", "victoria",
    "gol", "clasificamos", "clasificaron", "brillante", "increible",
    "espectacular", "historico", "partidazo", "crack", "tremendo",
    "vamos", "arriba", "excelente", "genial", "fenomenal"
]

# Palabras claramente negativas en contexto futbolístico
PALABRAS_NEGATIVAS = [
    "robo", "vergüenza", "verguenza", "eliminados", "perdimos",
    "perdieron", "fracaso", "desastre", "horrible", "injusto",
    "arbitro vendido", "mal arbitraje", "expulsado injusto",
    "pateticos", "decepcion", "derrota", "humillacion"
]

def detectar_sentimiento_por_palabras(texto):
    """Detecta sentimiento basado en palabras clave para casos simples."""
    texto_lower = texto.lower()
    palabras = texto_lower.split()
    
    puntos_positivos = sum(1 for p in PALABRAS_POSITIVAS if p in texto_lower)
    puntos_negativos = sum(1 for p in PALABRAS_NEGATIVAS if p in texto_lower)
    
    # Solo usar detección por palabras si hay señal clara y texto corto
    if len(palabras) <= 4:
        if puntos_positivos > puntos_negativos:
            return "positivo", 0.75
        elif puntos_negativos > puntos_positivos:
            return "negativo", 0.75
        else:
            return None, None
    
    return None, None

def preprocesar_texto(texto):
    """Maneja negaciones comunes en español."""
    negaciones = {
        "no estuvo mal": "estuvo bien",
        "no jugaron mal": "jugaron bien",
        "no fue tan malo": "fue aceptable",
        "no está mal": "está bien",
        "no estuvo tan mal": "estuvo bien",
        "nada mal": "bastante bien",
        "no tan malo": "aceptable",
        "mal tiro": "tiro fallado fracaso",
        "jugaron mal": "mal rendimiento fracaso",
        "jugamos mal": "mal rendimiento fracaso",
    }
    texto_lower = texto.lower()
    for negacion, reemplazo in negaciones.items():
        if negacion in texto_lower:
            texto = texto_lower.replace(negacion, reemplazo)
    return texto

class AnalizadorSentimiento:
    def __init__(self):
        print("Cargando modelo de sentimiento desde HuggingFace...")
        self.device = torch.device("cpu")
        self.tokenizador = AutoTokenizer.from_pretrained(MODELO_PATH)
        self.modelo = AutoModelForSequenceClassification.from_pretrained(
            MODELO_PATH,
            low_cpu_mem_usage=True
        )
        self.modelo.eval()
        print(f"Modelo cargado en: {self.device}")

    def analizar(self, texto):
        """Analiza el sentimiento de un comentario."""
        
        # Para textos muy cortos usar detección por palabras clave
        etiqueta_rapida, confianza_rapida = detectar_sentimiento_por_palabras(texto)
        if etiqueta_rapida:
            idx = list(ETIQUETAS.values()).index(etiqueta_rapida)
            probs = [0.1, 0.1, 0.1]
            probs[idx] = confianza_rapida
            return {
                "etiqueta": etiqueta_rapida,
                "confianza": confianza_rapida,
                "probabilidades": {
                    "negativo": probs[0],
                    "neutral": probs[1],
                    "positivo": probs[2]
                }
            }
        
        texto = preprocesar_texto(texto)
        encoding = self.tokenizador(
            texto,
            max_length=MAX_LENGTH,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.modelo(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        logits = outputs.logits
        probabilidades = torch.softmax(logits, dim=1).cpu().numpy()[0]

        UMBRAL_POSITIVO = 0.40
        if probabilidades[2] >= UMBRAL_POSITIVO:
            prediccion = 2
        elif probabilidades[0] >= probabilidades[1]:
            prediccion = 0
        else:
            prediccion = 1

        etiqueta = ETIQUETAS[prediccion]

        return {
            "etiqueta": etiqueta,
            "confianza": float(probabilidades[prediccion]),
            "probabilidades": {
                "negativo": float(probabilidades[0]),
                "neutral": float(probabilidades[1]),
                "positivo": float(probabilidades[2])
            }
        }

    def analizar_lote(self, textos):
        """Analiza múltiples comentarios."""
        resultados = []
        for texto in textos:
            resultado = self.analizar(texto)
            resultado["texto"] = texto
            resultados.append(resultado)
        return resultados