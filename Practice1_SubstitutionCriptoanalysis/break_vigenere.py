from basics import to_letters
from vigenere import cosets
import vigenere
from break_caesar import break_caesar
 
 
def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    groups = cosets(ciphertext, m)
    key_letters = []
    for group in groups:
        result = break_caesar(group, language)
        shift = result[0] #no nos importa el plaintext, solo nos interesa el shift que nos da el break_caesar
        letter = to_letters([shift])
        key_letters.append(letter)
 
    key = "".join(key_letters)
    plaintext = vigenere.decrypt(ciphertext, key)
 
    return key, plaintext