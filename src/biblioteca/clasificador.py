CATEGORIAS = {
    "Analisis Tecnico": [
        "rsi",
        "macd",
        "media movil",
        "soporte",
        "resistencia",
        "vela",
        "candlestick",
        "indicador",
        "tendencia",
        "divergencia"
    ],

    "Psicologia del Trading": [
        "miedo",
        "emociones",
        "disciplina",
        "confianza",
        "psicologia",
        "ansiedad",
        "mentalidad"
    ],

    "Gestion de Riesgo": [
        "riesgo",
        "stop loss",
        "capital",
        "drawdown",
        "apalancamiento",
        "perdida"
    ],

    "Inversion": [
        "accion",
        "etf",
        "dividendo",
        "empresa",
        "portafolio"
    ],

    "Historia de Mercados": [
        "historia",
        "crisis",
        "wall street",
        "livermore"
    ]
}

def clasificar_pregunta(pregunta):

    pregunta = pregunta.lower()

    print(f"\nPregunta recibida: {pregunta}")

    mejor_categoria = "Trading General"
    mejor_score = 0

    for categoria, palabras in CATEGORIAS.items():

        score = 0

        for palabra in palabras:

            if palabra in pregunta:
                print(f"Coincidencia: {palabra} -> {categoria}")
                score += 1

        print(f"{categoria}: {score}")

        if score > mejor_score:
            mejor_score = score
            mejor_categoria = categoria

    return mejor_categoria

if __name__ == "__main__":
    pregunta = input("Preguntas: ")
    categoria = clasificar_pregunta(pregunta)
    
    print(f"\nCategoria: {categoria}")
    