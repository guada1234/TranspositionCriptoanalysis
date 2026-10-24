import math
import random
import time
from itertools import permutations
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters
from columnar import encrypt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# construye la tabla que dice lo normal que es cada pareja de letras en inglés
def cargar_bigramas():
    texto = to_letters(to_numbers(open("referencia.txt", encoding="utf-8").read()))
    division = texto[:len(texto) // 2]

    cuentas = {}
    for a in ALPHABET:
        for b in ALPHABET:
            cuentas[a + b] = 1   # empiezo en 1 para que ningun par tenga probabilidad 0
    for i in range(len(division) - 1):
        cuentas[division[i:i + 2]] += 1

    total = sum(cuentas.values())
    bigramas = {}
    for par in cuentas:
        bigramas[par] = math.log(cuentas[par] / total)
    return bigramas


bigramas = cargar_bigramas()


def decrypt_orden(ciphertext, orden):
    columnas = len(orden)
    filas = len(ciphertext) // columnas
    matriz = [['' for _ in range(columnas)] for _ in range(filas)]
    k = 0
    for numero in range(1, columnas + 1):
        col = orden.index(numero)
        for fila in range(filas):
            matriz[fila][col] = ciphertext[k]
            k += 1
    resultado = ""
    for fila in range(filas):
        for col in range(columnas):
            resultado += matriz[fila][col]
    return resultado

# prueba todos los órdenes posibles y se queda con el que da el texto más parecido al inglés
def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    ciphertext = to_letters(to_numbers(ciphertext))
    mejor_orden = None
    mejor_texto = None
    mejor_score = None
    for orden in permutations(range(1, n_cols + 1)):
        candidato = decrypt_orden(ciphertext, orden)
        score = 0
        for i in range(len(candidato) - 1):
            score += bigramas[candidato[i:i + 2]]
        if mejor_score is None or score > mejor_score:
            mejor_score = score
            mejor_orden = orden
            mejor_texto = candidato
    return mejor_orden, mejor_texto


if __name__ == "__main__":
    texto = to_letters(to_numbers(open("referencia.txt", encoding="utf-8").read()))
    mitad = len(texto) // 2
    random.seed(1)

    for n_cols in [4, 5, 6, 7]:
        for largo in [60, 120, 200]:
            aciertos = 0
            for _ in range(100):
                clave = ""
                for _ in range(n_cols):
                    clave += random.choice(ALPHABET)
                inicio = random.randint(mitad, len(texto) - largo)   # solo de la segunda mitad
                original = texto[inicio:inicio + largo]
                orden, recuperado = attack(encrypt(original, clave), n_cols)
                if recuperado.startswith(original):   # lo que sobra al final son las X del relleno
                    aciertos += 1
            print(n_cols, "columnas,", largo, "letras:", aciertos, "%")

    for n_cols in [7, 8, 9]:
        inicio = time.time()
        attack(encrypt(texto[mitad:mitad + 200], ALPHABET[:n_cols]), n_cols)
        print(n_cols, "columnas:", round(time.time() - inicio, 1), "segundos")