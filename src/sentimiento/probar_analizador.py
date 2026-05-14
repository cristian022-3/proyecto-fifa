import sys
sys.path.append(".")
from src.sentimiento.analizador import AnalizadorSentimiento

analizador = AnalizadorSentimiento()

comentarios = [
    "¡Golazo histórico, campeones del mundo!",
    "Qué robo de árbitro, gol invalidado injustamente",
    "Colombia tuvo 60% de posesión en el primer tiempo",
    "¡Qué vergüenza de equipo, eliminados en primera ronda!",
    "El partido terminó 2-1 con gol en el minuto 89"
]

print("\n" + "="*50)
print("PRUEBA DEL ANALIZADOR DE SENTIMIENTO")
print("="*50)

for comentario in comentarios:
    resultado = analizador.analizar(comentario)
    print(f"\nComentario: {comentario}")
    print(f"Sentimiento: {resultado['etiqueta'].upper()}")
    print(f"Confianza:   {resultado['confianza']*100:.1f}%")
    print(f"Probabilidades: Neg={resultado['probabilidades']['negativo']:.3f} "
          f"Neu={resultado['probabilidades']['neutral']:.3f} "
          f"Pos={resultado['probabilidades']['positivo']:.3f}")

print("\n" + "="*50)
print("PRUEBA COMPLETADA")
print("="*50)