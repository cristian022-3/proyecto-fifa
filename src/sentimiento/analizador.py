import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ── Configuración ──────────────────────────────────────────
MODELO_PATH = os.getenv("MODELO_HF", "Cristian022/proyecto-fifa-sentimiento")
ETIQUETAS = {0: "negativo", 1: "neutral", 2: "positivo"}
MAX_LENGTH = 128
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
        print("Cargando modelo de sentimiento...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizador = AutoTokenizer.from_pretrained(MODELO_PATH)
        self.modelo = AutoModelForSequenceClassification.from_pretrained(MODELO_PATH)
        self.modelo = self.modelo.to(self.device)
        self.modelo.eval()
        print(f"Modelo cargado en: {self.device}")

    def analizar(self, texto):
        """Analiza el sentimiento de un comentario."""
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
        # Umbral ajustado para mejorar sensibilidad en positivos
        UMBRAL_POSITIVO = 0.40  # Más sensible que el default 0.5

        if probabilidades[2] >= UMBRAL_POSITIVO:
            prediccion = 2  # positivo
        elif probabilidades[0] >= probabilidades[1]:
            prediccion = 0  # negativo
        else:
            prediccion = 1  # neutral
        etiqueta = ETIQUETAS[prediccion]

        # Attention map para explicabilidad
        attention = outputs.attentions if hasattr(outputs, 'attentions') else None

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