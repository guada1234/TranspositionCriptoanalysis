def encrypt(plaintext: str, rails: int) -> str:
    if rails <= 1:
        return plaintext

    filas = rails
    columnas = len(plaintext) // filas + (len(plaintext) % filas > 0)
    matriz = [['' for _ in range(columnas)] for _ in range(filas)]
    direccion = 1 # indica la dirección del movimiento (1 para abajo, -1 para arriba)
    rail_actual = 0
    columna_actual = 0

    for char in plaintext:
        matriz[rail_actual][columna_actual] = char
        rail_actual += direccion

        if rail_actual == 0 or rail_actual == filas - 1:
            direccion *= -1
            columna_actual += 1

    ciphertext = ''.join(''.join(fila) for fila in matriz)
    return ciphertext


def decrypt(ciphertext: str, rails: int) -> str:
    if rails <= 1:
        return ciphertext

    filas = rails
    columnas = len(ciphertext) // filas + (len(ciphertext) % filas > 0)
    matriz = [['' for _ in range(columnas)] for _ in range(filas)]
    direccion = 1 # indica la dirección del movimiento (1 para abajo, -1 para arriba)
    rail_actual = 0
    columna_actual = 0

    for char in ciphertext:
        matriz[rail_actual][columna_actual] = char
        rail_actual += direccion

        if rail_actual == 0 or rail_actual == filas - 1:
            direccion *= -1
            columna_actual += 1

    plaintext = ''.join(''.join(fila) for fila in matriz)
    return plaintext



    