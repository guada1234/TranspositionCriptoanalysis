import affine
from break_caesar import chi_squared, ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES
 
 
def break_affine(ciphertext: str, language: str = "en") -> tuple[tuple[int, int], str]:
    if language == "en":
        table = ENGLISH_FREQUENCIES
    elif language == "es":
        table = SPANISH_FREQUENCIES
    else:
        raise ValueError(f"unknown language '{language}', use 'en' for English or 'es' for Spanish")
 
    best_key = None
    best_score = None
    best_plaintext = None
 
    for (a, b) in affine.valid_keys():#en estte caso, probamos con cada una de las claves validas (a,b)
        new_decrypt = affine.decrypt(ciphertext, a, b)
        score = chi_squared(new_decrypt, table)
 
        if best_score is None or score < best_score:
            best_key = (a, b)
            best_score = score
            best_plaintext = new_decrypt
 
    return best_key, best_plaintext