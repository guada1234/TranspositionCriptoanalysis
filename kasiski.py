from Practice1_SubstitutionCriptoanalysis.basics import *
from Practice1_SubstitutionCriptoanalysis.break_caesar import *


def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    sin_espacios = to_letters(to_numbers(ciphertext))
    repeticiones = {}
    largo = min_len

    while largo <= len(sin_espacios):
        posiciones = {}
        for i in range(len(sin_espacios) - largo + 1):
            sub_str = sin_espacios[i:i + largo]
            if sub_str not in posiciones:
                posiciones[sub_str] = []
            posiciones[sub_str].append(i)

        hay_repetidos = False
        for sub_str in posiciones:
            if len(posiciones[sub_str]) > 1:
                repeticiones[sub_str] = posiciones[sub_str]
                hay_repetidos = True

        if not hay_repetidos:
            break
        largo += 1

    return repeticiones


def distances(ciphertext: str, min_len: int = 3) -> list[int]:
    repeticiones = repeats(ciphertext, min_len)
    distancias = []

    for posiciones in repeticiones.values():
        for i in range(len(posiciones) - 1):
            distancia = posiciones[i + 1] - posiciones[i]
            distancias.append(distancia)

    distancias_sin_repetir = []
    for d in distancias:
        if d not in distancias_sin_repetir:
            distancias_sin_repetir.append(d)
    return distancias_sin_repetir



def factor_tally(ciphertext: str, max_factor: int = 20) -> dict[int, int]:
    distancias = distances(ciphertext)
    recuento = {}

    for factor in range(2, max_factor + 1): # prueba todos los factores desde 2 hasta max_factor incluido
        votos = 0
        for d in distancias:
            if d % factor == 0:     
                votos += 1
        recuento[factor] = votos

    return recuento

