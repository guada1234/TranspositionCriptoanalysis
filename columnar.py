import math
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
    n = len(plaintext)
    r = math.isqrt(n)
    if r * r == n:
        dimensiones = r
    else:
        dimensiones = r + 1

    texto = plaintext
    while len(texto) < dimensiones * dimensiones:
        texto += pad

    matriz = [['' for _ in range(dimensiones)] for _ in range(dimensiones)]
    k = 0
    for fila in range(dimensiones):
        for col in range(dimensiones):
            matriz[fila][col] = texto[k]
            k += 1

    orden = key_order(keyword)
    resultado = ""
    for numero in range(1, len(orden) + 1):
        col = orden.index(numero)    
        for j in range(dimensiones):
            resultado += matriz[j][col]
    return resultado

def decrypt(ciphertext: str, keyword: str) -> str:
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
    primera = encrypt(plaintext, kw1, pad)
    segunda = encrypt(primera, kw2, pad)
    return segunda


def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str:
    primera = decrypt(ciphertext, kw2)
    segunda = decrypt(primera, kw1)
    return segunda




