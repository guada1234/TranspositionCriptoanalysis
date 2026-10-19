from Practice1_SubstitutionCriptoanalysis.measure import chi_squared, ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES

def index_of_coincidence(text: str) -> float:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.upper()

    letras = ""
    for c in text:
        if c in ALPHABET:
            letras += c

    n = len(letras)
    if n < 2:
        return 0.0      # con 0 o 1 letras no se pueden formar parejas

    # Numerador: parejas de letras iguales
    suma = 0
    for letra in ALPHABET:
        cantidad = letras.count(letra)
        suma += cantidad * (cantidad - 1)

    # Denominador: todas las parejas posibles
    return suma / (n * (n - 1))


def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""
    if language == "es":
        tabla = SPANISH_FREQUENCIES
    else:
        tabla = ENGLISH_FREQUENCIES
    if chi_squared(ciphertext, tabla) < UMBRAL:
        return "transposition"
    return "substitution"