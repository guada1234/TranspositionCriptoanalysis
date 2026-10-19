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



def hacer_muestras(texto, largo, padding_aleatorio):
    """150 transposiciones y 150 sustituciones de un largo dado.
    Devuelve una lista de (puntuacion, tipo_real)."""
    muestras = []
    for _ in range(150):
        # --- Transposición por columnas con clave aleatoria ---
        inicio = random.randint(0, len(texto) - largo)
        trozo = texto[inicio:inicio + largo]
 
        clave = ""
        for _ in range(random.randint(4, 8)):
            clave += random.choice(ALPHABET)
 
        if padding_aleatorio:
            # Rellenamos con letras al azar según las frecuencias del inglés
            letras = list(ENGLISH_FREQUENCIES.keys())
            pesos = list(ENGLISH_FREQUENCIES.values())
            while len(trozo) % len(clave) != 0:
                trozo += random.choices(letras, weights=pesos)[0]
 
        cifrado = encrypt(trozo, clave, "X")
        muestras.append((chi_squared(cifrado, ENGLISH_FREQUENCIES), "transposition"))
 
        # --- Sustitución monoalfabética con clave aleatoria ---
        inicio = random.randint(0, len(texto) - largo)
        trozo = texto[inicio:inicio + largo]
 
        alfabeto_desordenado = list(ALPHABET)
        random.shuffle(alfabeto_desordenado)
 
        cifrado = ""
        for letra in trozo:
            cifrado += alfabeto_desordenado[ALPHABET.index(letra)]
        muestras.append((chi_squared(cifrado, ENGLISH_FREQUENCIES), "substitution"))
    return muestras

 # ----------------------------------------------------------------------------------------------------
 
def contar_errores(muestras, umbral):
    errores = 0
    for puntuacion, tipo_real in muestras:
        if puntuacion < umbral:
            prediccion = "transposition"
        else:
            prediccion = "substitution"
        if prediccion != tipo_real:
            errores += 1
    return errores
 
 
def elegir_umbral(muestras):
    """Prueba umbrales de 0.00 a 5.00 y devuelve el que comete menos errores."""
    mejor_umbral = 0
    menos_errores = len(muestras)
    for i in range(501):
        umbral = i / 100
        errores = contar_errores(muestras, umbral)
        if errores < menos_errores:
            menos_errores = errores
            mejor_umbral = umbral
    return mejor_umbral
 
 
if __name__ == "__main__":
    with open("referencia.txt", encoding="utf-8") as f:
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texto = ""
        for c in f.read().upper():
            if c in ALPHABET:
                texto += c
 
    print("Letras en el texto de referencia:", len(texto))
    if len(texto) < 700:
        raise ValueError("El texto de referencia necesita al menos 700 letras")
 
    largos = [60, 120, 250, 400]
    errores_por_padding = {}
 
    for padding_aleatorio in [False, True]:
        # 1. Generar todas las muestras
        muestras_por_largo = {}
        todas = []
        for largo in largos:
            muestras_por_largo[largo] = hacer_muestras(texto, largo, padding_aleatorio)
            todas += muestras_por_largo[largo]
 
        # 2. Elegir el umbral a partir de los datos
        umbral = elegir_umbral(todas)
        if padding_aleatorio:
            print("Padding aleatorio: umbral =", umbral)
        else:
            print("Padding X: umbral =", umbral)
 
        # 3. Tasa de error para cada largo
        tasas = {}
        for largo in largos:
            muestras = muestras_por_largo[largo]
            tasas[largo] = contar_errores(muestras, umbral) / len(muestras)
        errores_por_padding[padding_aleatorio] = tasas
 
    print()
    print("Largo | Error pad X | Error pad aleatorio")
    for largo in largos:
        x = errores_por_padding[False][largo]
        r = errores_por_padding[True][largo]
        print(f"{largo:5} | {x:11.1%} | {r:19.1%}")