from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters


def encrypt(plaintext: str, rails: int) -> str:
    plaintext = to_letters(to_numbers(plaintext))  # mayúsculas y solo letras
    if rails <= 1:
        return plaintext

    filas = rails
    columnas = len(plaintext) // (filas - 1) + 1   # en cada columna caben filas - 1 letras
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
    ciphertext = to_letters(to_numbers(ciphertext))  # mayúsculas y solo letras
    if rails <= 1:
        return ciphertext

    filas = rails
    columnas = len(ciphertext) // (filas - 1) + 1
    matriz = [['' for _ in range(columnas)] for _ in range(filas)]

    # 1. Recorrer el mismo zigzag que encrypt, marcando las casillas que se usan
    direccion = 1
    rail_actual = 0
    columna_actual = 0
    for _ in ciphertext:
        matriz[rail_actual][columna_actual] = '*'
        rail_actual += direccion

        if rail_actual == 0 or rail_actual == filas - 1:
            direccion *= -1
            columna_actual += 1

    # 2. Rellenar las casillas marcadas fila por fila (así se leyó al cifrar)
    k = 0
    for fila in range(filas):
        for col in range(columnas):
            if matriz[fila][col] == '*':
                matriz[fila][col] = ciphertext[k]
                k += 1

    # 3. Volver a recorrer el zigzag, leyendo las letras en el orden original
    plaintext = ''
    direccion = 1
    rail_actual = 0
    columna_actual = 0
    for _ in ciphertext:
        plaintext += matriz[rail_actual][columna_actual]
        rail_actual += direccion

        if rail_actual == 0 or rail_actual == filas - 1:
            direccion *= -1
            columna_actual += 1

    return plaintext