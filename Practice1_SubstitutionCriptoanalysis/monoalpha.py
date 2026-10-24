from basics import to_numbers, to_letters, modinv, egcd

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def check_valid_key(key: str) -> str:
    key = key.upper()

    if len(key) != 26:                          
        raise ValueError("key must be a 26-letter permutation of A-Z")

    for letter in ALPHABET: #todas las letras qienen que aparecer una solo vez en la clave
        if letter not in key:                 
            raise ValueError("key must be a 26 letter permutation of A-Z")
    return key

def encrypt(plaintext: str, key: str) -> str:
    key = check_valid_key(key)
    numbers = to_numbers(plaintext)
    result = []
    for n in numbers:
        substitute = key[n] #key[n] nos da la letra correspondiente a la posicion n en la clave
        result.append(substitute)
    return "".join(result)


def decrypt(ciphertext: str, key: str) -> str:
    key = check_valid_key(key)
    numbers = to_numbers(ciphertext)
    result = []                                 
    for n in numbers:                         
        cipher_letter = ALPHABET[n] #obtenemos la letra correspondiente a la posicion n en el alfabeto
        position = key.index(cipher_letter) #buscamos la posicion de la letra en la clave, que nos da el numero correspondiente a la letra original
        result.append(ALPHABET[position]) 
 
    return "".join(result)




def key_from_keyword(keyword: str) -> str:
    keyword = keyword.upper()
    final_key = []
    for char in keyword:
        if "A" <= char <= "Z" and char not in final_key:
            final_key.append(char)
 
    for char in ALPHABET:
        if char not in final_key:
            final_key.append(char) #rellenamos el resto de la clave con las letras que no estan en la palabra clave, en orden alfabetico
 
    return "".join(final_key)
