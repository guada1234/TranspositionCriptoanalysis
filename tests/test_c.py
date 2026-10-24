import os
import random
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters
from Practice1_SubstitutionCriptoanalysis.vigenere import encrypt as vigenere_encrypt
from columnar import encrypt as columnar_encrypt
import keylength
import break_vigenere
import break_columnar

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTO = to_letters(to_numbers(open(os.path.join(CARPETA, "referencia.txt"), encoding="utf-8").read()))


def clave_aleatoria(largo):
    clave = ""
    for _ in range(largo):
        clave += random.choice(ALPHABET)
    return clave


def trozo(largo):
    inicio = random.randint(0, len(TEXTO) - largo)
    return TEXTO[inicio:inicio + largo]


# Largos elegidos donde las tablas de la parte C dicen que el ataque es fiable (N >= 40 * m)

def test_find_key_length_20_textos():
    random.seed(4)
    for _ in range(20):
        clave = clave_aleatoria(5)
        assert keylength.find_key_length(vigenere_encrypt(trozo(400), clave)) == 5


def test_coset_ic_alto_en_el_largo_real():
    random.seed(5)
    cifrado = vigenere_encrypt(trozo(400), "LEMON")
    assert keylength.coset_ic(cifrado, 5) > keylength.coset_ic(cifrado, 3)


def test_vigenere_attack_20_textos():
    random.seed(6)
    for _ in range(20):
        clave = clave_aleatoria(5)
        original = trozo(400)
        clave_encontrada, texto = break_vigenere.attack(vigenere_encrypt(original, clave))
        assert clave_encontrada == clave
        assert texto == original


def test_columnar_attack_20_textos():
    random.seed(7)
    for _ in range(20):
        clave = clave_aleatoria(6)
        original = trozo(120)
        orden, texto = break_columnar.attack(columnar_encrypt(original, clave), 6)
        assert texto.startswith(original)     # lo que sobra al final es el relleno


def test_casos_limite_parte_c():
    assert keylength.find_key_length("") >= 1
    assert keylength.find_key_length("A") >= 1