from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters, modinv, egcd


def check_valid_key(key: str) -> str:
    key = key.upper()

    if len(key) == 0:                            
        raise ValueError("the key must not be empty")

    for char in key:   
        if not ("A" <= char <= "Z"):
            raise ValueError(f"the key must contain only letters, found '{char}'")

    return key


def encrypt(plaintext: str, key: str) -> str:
    key = check_valid_key(key) 
    key_numbers = to_numbers(key)
    plain_numbers = to_numbers(plaintext)
    result = []
    position = 0
    for n in plain_numbers:
        key_index = position % len(key_numbers) #para saber que letra de la clave usar, usamos el modulo para que se repita la clave si es mas corta que el texto
        shift = key_numbers[key_index]
        result.append(n + shift) #el shift ya no es siempre el mismo número k, sino que cambia en cada letra, siguiendo la clave
        position = position + 1

    return to_letters(result)

def decrypt(ciphertext: str, key: str) -> str:
    key = check_valid_key(key) 
    key_numbers = to_numbers(key)
    cipher_numbers = to_numbers(ciphertext)
    result = []
    position = 0
    for n in cipher_numbers:
        key_index = position % len(key_numbers)
        shift = key_numbers[key_index]
        result.append(n - shift) 
        position = position + 1

    return to_letters(result)


#todas las letras de un mismo grupo tienen que ser desplazadas por la misma letra de la clave
def cosets(ciphertext: str, m: int) -> list[str]:
    cipher_numbers = to_numbers(ciphertext)
    groups = []
    for i in range(m): #creamos una lista vacía por posición dentro de la clave
        groups.append([])

    position = 0
    for n in cipher_numbers:
        group_index = position % m #usando position % m veo a qué grupo pertenece cada letra
        groups[group_index].append(n)
        position = position + 1

    result = []
    for group in groups:
        result.append(to_letters(group))

    return result






