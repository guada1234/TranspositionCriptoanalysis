import math
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters


def key_order(keyword: str) -> list[int]:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keyword = keyword.upper()
    lista = []
    for i in range(len(keyword)):
        if keyword[i] in ALPHABET:
            valor = ALPHABET.index(keyword[i])
            numero = 1
            for j in range(len(keyword)):
                otro = ALPHABET.index(keyword[j])
                if otro < valor or (otro == valor and j < i):
                    numero += 1
            lista.append(numero)
    return lista


def encrypt(plaintext: str, keyword: str, pad: str = "X") -> str:
    plaintext = to_letters(to_numbers(plaintext))   # mayúsculas y solo letras
    n = len(plaintext)
    columnas = len(keyword)
    filas = (n + columnas - 1) // columnas

    # Rellenar con pad hasta completar la matriz
    total = filas * columnas
    faltan = total - n
    relleno = pad * faltan
    texto = plaintext + relleno

    # Escribir el texto en la matriz fila por fila
    matriz = [['' for _ in range(columnas)] for _ in range(filas)]
    for f in range(filas):
        for c in range(columnas):
            matriz[f][c] = texto[f * columnas + c]

    # Leer columna por columna, en el orden de key_order
    orden = key_order(keyword)
    resultado = ""
    for numero in range(1, columnas + 1):
        c = orden.index(numero)
        for f in range(filas):
            resultado += matriz[f][c]
    return resultado


def decrypt(ciphertext: str, keyword: str) -> str:
    ciphertext = to_letters(to_numbers(ciphertext))  # mayúsculas y solo letras
    columnas = len(keyword)
    largo = len(ciphertext)
    if largo % columnas != 0:
        raise ValueError("El largo del texto cifrado no es múltiplo del largo de la clave")
    filas = largo // columnas

    matriz = [['' for _ in range(columnas)] for _ in range(filas)]
    orden = key_order(keyword)
    k = 0
    for numero in range(1, len(orden) + 1):
        col = orden.index(numero)
        for fila in range(filas):
            matriz[fila][col] = ciphertext[k]
            k += 1

    resultado = ""
    for fila in range(filas):
        for col in range(columnas):
            resultado += matriz[fila][col]
    return resultado


def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str:
    # Se rellena una sola vez, hasta un múltiplo de los dos largos de clave,
    # para que ninguna de las dos pasadas tenga que añadir relleno propio
    plaintext = to_letters(to_numbers(plaintext))
    multiplo = math.lcm(len(kw1), len(kw2))
    while len(plaintext) % multiplo != 0:
        plaintext += pad
    primera = encrypt(plaintext, kw1, pad)
    segunda = encrypt(primera, kw2, pad)
    return segunda


def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str:
    primera = decrypt(ciphertext, kw2)
    segunda = decrypt(primera, kw1)
    return segunda