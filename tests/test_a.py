import random
import pytest
import railfence
import columnar

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def texto_aleatorio(largo):
    texto = ""
    for _ in range(largo):
        texto += random.choice(ALPHABET)
    return texto


# ---------- A1: rail fence ----------

def test_railfence_valores_del_enunciado():
    assert railfence.encrypt("MYSECRETMESSAGE", 2) == "MSCEMSAEYERTESG"
    assert railfence.encrypt("MYSECRETMESSAGE", 3) == "MCMAYERTESGSESE"
    assert railfence.encrypt("MYSECRETMESSAGE", 4) == "MEAYRTSGSCMSEEE"


def test_railfence_ida_y_vuelta():
    random.seed(0)
    for _ in range(200):
        texto = texto_aleatorio(random.randint(1, 60))
        rails = random.randint(2, 10)
        assert railfence.decrypt(railfence.encrypt(texto, rails), rails) == texto


def test_railfence_normaliza():
    assert railfence.decrypt(railfence.encrypt("my secret, message!", 3), 3) == "MYSECRETMESSAGE"


# ---------- A2: columnar ----------

def test_key_order_valores_del_enunciado():
    assert columnar.key_order("ENIGMA") == [2, 6, 4, 3, 5, 1]
    assert columnar.key_order("ROTOR") == [3, 1, 5, 2, 4]
    assert columnar.key_order("KASISKI") == [4, 1, 6, 2, 7, 5, 3]
    assert columnar.key_order("BLETCHLEY") == [1, 6, 3, 8, 2, 5, 7, 4, 9]


def test_columnar_valores_del_enunciado():
    assert columnar.encrypt("MYSECRETMESSAGE", "CIPHER") == "MEACSXEEXYTGSMERSX"
    assert columnar.encrypt("THE INDEX OF COINCIDENCE", "KASISKI") == "HOIICEENETXCDICEFDNON"


def test_columnar_ida_y_vuelta_devuelve_texto_con_relleno():
    random.seed(1)
    for _ in range(200):
        texto = texto_aleatorio(random.randint(1, 60))
        clave = texto_aleatorio(random.randint(2, 9))
        descifrado = columnar.decrypt(columnar.encrypt(texto, clave), clave)
        assert descifrado.startswith(texto)
        assert set(descifrado[len(texto):]) <= {"X"}     # lo que sobra es solo relleno
        assert len(descifrado) % len(clave) == 0


def test_columnar_pad_es_un_parametro():
    assert columnar.encrypt("ABCDE", "KEY", "Q").count("Q") == 1


# ---------- A3: doble transposición ----------

def test_doble_valor_del_enunciado():
    resultado = columnar.encrypt_double("THESAMEKEYMUSTNEVERBEUSEDTWICE", "ROTOR", "ENIGMA")
    assert resultado == "WCTEIHSTAEVREBEUTMNSUEEDSEEMYK"


def test_doble_largo_no_multiplo_de_ninguna_clave():
    texto = "THESAMEKEYMUSTNEVERBEUSEDTWICEAB"     # 32 letras: no es múltiplo de 3 ni de 7
    cifrado = columnar.encrypt_double(texto, "ABC", "KASISKI")
    assert columnar.decrypt_double(cifrado, "ABC", "KASISKI").startswith(texto)


def test_doble_ida_y_vuelta():
    random.seed(2)
    for _ in range(200):
        texto = texto_aleatorio(random.randint(1, 60))
        kw1 = texto_aleatorio(random.randint(2, 8))
        kw2 = texto_aleatorio(random.randint(2, 8))
        descifrado = columnar.decrypt_double(columnar.encrypt_double(texto, kw1, kw2), kw1, kw2)
        assert descifrado.startswith(texto)
        assert set(descifrado[len(texto):]) <= {"X"}


# ---------- Casos límite ----------

def test_texto_vacio():
    assert railfence.encrypt("", 3) == ""
    assert railfence.decrypt("", 3) == ""
    assert columnar.encrypt("", "KEY") == ""
    assert columnar.decrypt("", "KEY") == ""


def test_una_sola_letra():
    assert railfence.decrypt(railfence.encrypt("A", 3), 3) == "A"
    assert columnar.decrypt(columnar.encrypt("A", "KEY"), "KEY") == "AXX"


def test_sin_letras():
    assert railfence.encrypt("123 !?", 3) == ""
    assert columnar.encrypt("123 !?", "KEY") == ""


def test_cifrado_mas_corto_que_las_columnas():
    with pytest.raises(ValueError):
        columnar.decrypt("AB", "CIPHER")