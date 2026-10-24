import os
import random
import measure
import kasiski
from columnar import encrypt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

KASISKI_TEXTO = """ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL
ELQYR JXAOA LPKGV D"""


# ---------- B1: índice de coincidencia ----------

def test_ic_valores_del_enunciado():
    assert abs(measure.index_of_coincidence("CRYPTANALYSIS") - 6 / 156) < 1e-9
    assert abs(measure.index_of_coincidence("THEINDEXOFCOINCIDENCE") - 34 / 420) < 1e-9


def test_ic_casos_limite():
    assert measure.index_of_coincidence("") == 0.0
    assert measure.index_of_coincidence("A") == 0.0
    assert measure.index_of_coincidence("123 !?") == 0.0


# ---------- B2: clasificador ----------

def test_classify():
    # El clasificador tiene un pequeño error medido en el B2 (unos pocos %),
    # así que se permiten como mucho 2 fallos de 40.
    
    carpeta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    texto = open(os.path.join(carpeta, "referencia.txt"), encoding="utf-8").read()
    texto = "".join(c for c in texto.upper() if c in ALPHABET)
    random.seed(3)
    fallos = 0
    for _ in range(20):
        inicio = random.randint(0, len(texto) - 400)
        trozo = texto[inicio:inicio + 400]
        if measure.classify(encrypt(trozo, "CIPHER")) != "transposition":
            fallos += 1
        desordenado = list(ALPHABET)
        random.shuffle(desordenado)
        sustitucion = "".join(desordenado[ALPHABET.index(c)] for c in trozo)
        if measure.classify(sustitucion) != "substitution":
            fallos += 1
    assert fallos <= 2


# ---------- B3: Kasiski ----------

def test_kasiski_repeats():
    r = kasiski.repeats(KASISKI_TEXTO)
    assert r["ELQ"] == [0, 15, 50]
    assert r["ELQYRJ"] == [0, 50]
    mas_largo = max(r, key=len)
    assert mas_largo == "ELQYRJ"


def test_kasiski_distances():
    assert sorted(kasiski.distances(KASISKI_TEXTO)) == [15, 35, 50]


def test_kasiski_factor_tally():
    tally = kasiski.factor_tally(KASISKI_TEXTO)
    assert tally[5] == 3
    assert max(tally, key=tally.get) == 5


def test_kasiski_texto_vacio():
    assert kasiski.repeats("") == {}
    assert kasiski.distances("") == []