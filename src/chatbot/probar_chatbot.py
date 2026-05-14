import sys
sys.path.append(".")
from src.chatbot.chatbot import ChatbotFIFA

# Iniciar chatbot
chatbot = ChatbotFIFA()

# Preguntas de prueba
preguntas = [
    "¿Cuánto dura un partido de fútbol?",
    "¿Qué es el fuera de juego?",
    "¿Cuándo se cobra un penal?",
    "¿Qué es el VAR?",
    "¿Cuál es la receta del arroz con leche?"
]

print("\n" + "="*50)
print("PRUEBA DEL CHATBOT FIFA")
print("="*50)

for pregunta in preguntas:
    print(f"\nPregunta: {pregunta}")
    print("-"*40)
    print("Respuesta: ", end="", flush=True)
    
    respuesta_completa = ""
    for fragmento in chatbot.responder_stream(pregunta):
        print(fragmento, end="", flush=True)
        respuesta_completa += fragmento
    
    print("\n")

print("="*50)
print("PRUEBA COMPLETADA")
print("="*50)