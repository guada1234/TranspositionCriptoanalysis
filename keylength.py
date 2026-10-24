import random
import os
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters
from Practice1_SubstitutionCriptoanalysis.vigenere import cosets, encrypt as vigenere_encrypt
from Practice1_SubstitutionCriptoanalysis.break_caesar import ALPHABET, ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES
from measure import index_of_coincidence

CARPETA = os.path.dirname(os.path.abspath(__file__))


def coset_ic(ciphertext: str, m: int) -> float:
    grupos = cosets(ciphertext, m)
    suma = 0.0
    for grupo in grupos:
        suma += index_of_coincidence(grupo)
    return suma / m


def calibrar_fraccion(mostrar=False):
    """Prueba varias fracciones con textos cifrados de clave conocida
    y devuelve la que más acierta."""
    texto = to_letters(to_numbers(open(os.path.join(CARPETA, "referencia.txt"), encoding="utf-8").read()))

    # IC del inglés y del azar
    ic_idioma = 0.0
    for letra in ENGLISH_FREQUENCIES:
        p = ENGLISH_FREQUENCIES[letra] / 100
        ic_idioma += p * p
    ic_aleatorio = 1 / 26

    # 1. Crear 200 textos cifrados de 400 letras, sabiendo el largo real de su clave
    random.seed(0)
    pruebas = []
    for _ in range(200):
        clave = ""
        for _ in range(random.randint(3, 10)):
            clave += random.choice(ALPHABET)
        inicio = random.randint(0, len(texto) - 400)
        cifrado = vigenere_encrypt(texto[inicio:inicio + 400], clave)
        pruebas.append((cifrado, len(clave)))

    # 2. Para cada fracción, contar cuántas veces acierta
    mejor_fraccion = 0
    mas_aciertos = 0
    for fraccion in [0.5, 0.6, 0.7, 0.8, 0.9]:
        umbral = ic_aleatorio + fraccion * (ic_idioma - ic_aleatorio)
        aciertos = 0
        for cifrado, largo_real in pruebas:
            # la m más pequeña que supera el umbral
            largo_encontrado = 1
            for m in range(1, 17):
                if coset_ic(cifrado, m) > umbral:
                    largo_encontrado = m
                    break
            if largo_encontrado == largo_real:
                aciertos += 1
        if mostrar:
            print(fraccion, aciertos, "de 200")
        if aciertos > mas_aciertos:
            mas_aciertos = aciertos
            mejor_fraccion = fraccion
    return mejor_fraccion


FRACCION = None   # se rellena la primera vez que se llama a find_key_length


def find_key_length(ciphertext: str, max_m: int = 16, language: str = "en") -> int:
    if language == "es":
        tabla = SPANISH_FREQUENCIES
    else:
        tabla = ENGLISH_FREQUENCIES

    # IC del idioma y del azar
    ic_idioma = 0.0
    for letra in tabla:
        p = tabla[letra] / 100
        ic_idioma += p * p
    ic_aleatorio = 1 / 26

    # La calibración se hace solo la primera vez y se guarda en FRACCION
    global FRACCION
    if FRACCION is None:
        FRACCION = calibrar_fraccion()

    # "Claramente por encima" = haber recorrido esa fracción del camino
    umbral = ic_aleatorio + FRACCION * (ic_idioma - ic_aleatorio)

    # La m más pequeña que supera el umbral
    for m in range(1, max_m + 1):
        if coset_ic(ciphertext, m) > umbral:
            return m
    return 1   # si ninguna lo supera


if __name__ == "__main__":
    # Tabla de calibración (informe C1)
    print("Fracción elegida:", calibrar_fraccion(mostrar=True))
    print()

    # Tabla de coset_ic para m = 1..16 con una clave conocida (informe C1)
    texto = to_letters(to_numbers(open(os.path.join(CARPETA, "referencia.txt"), encoding="utf-8").read()))
    clave = "CIPHER"      # largo 6: tiene divisores (2 y 3) y un múltiplo (12) hasta 16
    cifrado = vigenere_encrypt(texto[:600], clave)
    real = len(clave)
    for m in range(1, 17):
        if m == real:
            marca = "largo real"
        elif m % real == 0:
            marca = "múltiplo"
        elif real % m == 0:
            marca = "divisor"
        else:
            marca = ""
        print(f"m = {m:2}: {coset_ic(cifrado, m):.4f}  {marca}")