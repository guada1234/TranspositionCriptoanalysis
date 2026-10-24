import pytest
import vigenere


def test_check_values_from_handout():
    assert vigenere.encrypt("MYSECRETMESSAGE", "KEY") == "WCQOGPOXKOWQKKC"
    assert vigenere.encrypt("attackatdawn", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere.cosets("ABCDEF", 3) == ["AD", "BE", "CF"]


def test_roundtrip():
    plaintext = "THEQUICKBROWNFOX"
    assert vigenere.decrypt(vigenere.encrypt(plaintext, "KEY"), "KEY") == plaintext


def test_rejects_empty_key():
    with pytest.raises(ValueError):
        vigenere.encrypt("abc", "")


def test_rejects_key_with_non_letters():
    with pytest.raises(ValueError):
        vigenere.encrypt("abc", "KEY3")


def test_cosets_lengths_add_up_to_total_length():
    ciphertext = "ABCDEFGHIJ"          # 10 letters
    groups = vigenere.cosets(ciphertext, 3)
    total = 0
    for group in groups:
        total = total + len(group)
    assert total == len(ciphertext)


def test_key_shorter_than_text_repeats_correctly():
    import caesar
    plaintext = "HELLOWORLD"
    assert vigenere.encrypt(plaintext, "D") == caesar.encrypt(plaintext, 3)


def test_empty_input():
    assert vigenere.encrypt("", "KEY") == ""


def test_single_character():
    assert vigenere.decrypt(vigenere.encrypt("A", "KEY"), "KEY") == "A"


def test_input_with_no_letters():
    assert vigenere.encrypt("12345 !!! ,,,", "KEY") == ""


def test_input_shorter_than_vigenere_key():
    short_plaintext = "HI"
    long_key = "SECRET"
    ciphertext = vigenere.encrypt(short_plaintext, long_key)
    assert len(ciphertext) == 2
    assert vigenere.decrypt(ciphertext, long_key) == short_plaintext