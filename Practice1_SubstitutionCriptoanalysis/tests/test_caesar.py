import caesar

def test_check_value_from_handout():
    assert caesar.encrypt("MYSECRETMESSAGE", 3) == "PBVHFUHWPHVVDJH"


def test_roundtrip():
    plaintext = "HELLOWORLD"
    for k in [0, 1, 13, 25]:
        ciphertext = caesar.encrypt(plaintext, k)
        assert caesar.decrypt(ciphertext, k) == plaintext


def test_negative_and_large_shifts_still_work():
    plaintext = "HELLOWORLD"
    assert caesar.encrypt(plaintext, -3) == caesar.encrypt(plaintext, 23) 
    assert caesar.encrypt(plaintext, 30) == caesar.encrypt(plaintext, 4)


def test_input_is_normalised():
    assert caesar.encrypt("Hello, World!", 3) == caesar.encrypt("HELLOWORLD", 3)



def test_empty_input():
    assert caesar.encrypt("", 3) == ""


def test_single_character():
    assert caesar.encrypt("A", 1) == "B"
    assert caesar.decrypt(caesar.encrypt("A", 1), 1) == "A"


def test_input_with_no_letters():
    assert caesar.encrypt("12345 !!! ,,,", 3) == ""