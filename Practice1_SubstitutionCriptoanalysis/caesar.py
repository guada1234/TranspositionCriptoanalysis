from  Practice1_SubstitutionCriptoanalysis.basics  import to_numbers, to_letters


def encrypt(plaintext: str, k: int) -> str:
    numbers = to_numbers(plaintext)          #usamos la funcion de la parte A para convertir a numeros el texto
    shifted = []                        
    for n in numbers:                        
        shifted.append(n + k)                 # lo shifteamos sumandole la clave k
    
    return to_letters(shifted)             # convertimos el numero "shifteado" a letras y lo retornamos


def decrypt(ciphertext: str, k: int) -> str:
    numbers = to_numbers(ciphertext)          
    shifted = []                               
    for n in numbers:                          
        shifted.append(n - k)                  

    return to_letters(shifted)
