import random
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters
from Practice1_SubstitutionCriptoanalysis.vigenere import cosets, encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from Practice1_SubstitutionCriptoanalysis.break_caesar import break_caesar
from keylength import find_key_length

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    """Returns (key, plaintext). The key length is NOT given."""
    m = find_key_length(ciphertext, language=language)

    # partir en cosets y romper cada uno como un César
    key = ""
    for grupo in cosets(ciphertext, m):
        shift, _ = break_caesar(grupo, language)
        key += ALPHABET[shift]

    # descifrar con la clave encontrada
    plaintext = vigenere_decrypt(ciphertext, key)
    return key, plaintext


if __name__ == "__main__":
    texto = to_letters(to_numbers(open("referencia.txt", encoding="utf-8").read()))
    random.seed(1)

    largos_clave = [3, 5, 7, 9]
    largos_texto = [100, 150, 200, 300, 400]
    pruebas = 100

    tabla_clave = {}    # (m, N) -> clave completa correcta
    tabla_largo = {}    # (m, N) -> largo de clave correcto

    for m in largos_clave:
        for n in largos_texto:
            clave_ok = 0
            largo_ok = 0
            for _ in range(pruebas):
                # Clave aleatoria de largo m y trozo aleatorio de largo n
                clave = ""
                for _ in range(m):
                    clave += random.choice(ALPHABET)
                inicio = random.randint(0, len(texto) - n)
                cifrado = vigenere_encrypt(texto[inicio:inicio + n], clave)

                clave_encontrada, _ = attack(cifrado)
                if clave_encontrada == clave:
                    clave_ok += 1
                if len(clave_encontrada) == m:
                    largo_ok += 1
            tabla_clave[(m, n)] = clave_ok / pruebas
            tabla_largo[(m, n)] = largo_ok / pruebas

    for titulo, tabla in [("Clave completa recuperada", tabla_clave),
                          ("Largo de clave correcto", tabla_largo)]:
        print()
        print(titulo)
        print("clave \\ texto", end="")
        for n in largos_texto:
            print(f"{n:>7}", end="")
        print()
        for m in largos_clave:
            print(f"{m:>13}", end="")
            for n in largos_texto:
                print(f"{tabla[(m, n)]:>7.0%}", end="")
            print()