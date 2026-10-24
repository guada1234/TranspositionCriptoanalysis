
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers
from Practice1_SubstitutionCriptoanalysis import caesar

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_FREQUENCIES = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702,
    "F": 2.228, "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153,
    "K": 0.772, "L": 4.025, "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987, "S": 6.327, "T": 9.056,
    "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150, "Y": 1.974,
    "Z": 0.074,
}
 
SPANISH_FREQUENCIES = {
    "A": 12.53, "B": 1.42, "C": 4.68, "D": 5.86, "E": 13.68,
    "F": 0.69, "G": 1.01, "H": 0.70, "I": 6.25, "J": 0.44,
    "K": 0.11, "L": 4.97, "M": 3.15, "N": 6.71, "O": 8.68,
    "P": 2.51, "Q": 0.88, "R": 6.87, "S": 7.98, "T": 4.63,
    "U": 3.93, "V": 0.90, "W": 0.02, "X": 0.22, "Y": 0.90,
    "Z": 0.52,
}


#un descifrado incorrecto no cumple con las distribuciones propias del ingles o español
#probamos con todos los shifts posibles y nos quedamos con el que nos da un descifrado que cumple con las distribuciones propias del idioma 
def chi_squared(text: str, table: dict[str, float]) -> float:
    text_numbers = to_numbers(text)
    length = len(text_numbers)
 
    if length == 0:
        return 0.0
 
    counts = [0] * 26 #por cada letra del alfabeto, contamos cuantas veces aparece en el texto
    for n in text_numbers:
        counts[n] = counts[n] + 1
 
    total = 0.0
    for i in range(26):
        letter = ALPHABET[i]
        frecuency = table[letter]
        expected_count = (frecuency / 100.0) * length #pasamos la frecuencia a un valor entre 0 y 1, y lo multiplicamos por la longitud del texto para obtener el número esperado de apariciones de esa letra
        observed_count = counts[i]
        difference = (observed_count - expected_count) ** 2 / expected_count
        total = total + difference

    result = total / length #dividimos entre la longitud del texto para que no dependa de la longitud del texto, y podamos comparar entre textos de diferente longitud
    return result



def break_caesar(ciphertext: str, language: str = "en") -> tuple[int, str]:

    if language == "en":
        table = ENGLISH_FREQUENCIES
    elif language == "es":
        table = SPANISH_FREQUENCIES
    else:
        raise ValueError(f"unknown language '{language}', use 'en' for English or 'es' for Spanish")
 
    best_shift = None
    best_score = None
    best_plaintext = None
 
    for n in range(26):
        new_decrypt = caesar.decrypt(ciphertext, n) #desencriptamos con cada shift posible, y calculamos el chi cuadrado de cada uno para ver cual es el que mas se parece a la distribucion de frecuencias del idioma
        score = chi_squared(new_decrypt, table)
 
        if best_score is None or score < best_score:
            best_shift = n
            best_score = score
            best_plaintext = new_decrypt
 
    return best_shift, best_plaintext




