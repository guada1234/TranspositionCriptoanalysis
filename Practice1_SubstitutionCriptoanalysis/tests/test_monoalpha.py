import pytest
import monoalpha

KEY = "MNBVCXZASDFGHJKLPOIUYTREWQ"


def test_check_values_from_handout():
    assert monoalpha.key_from_keyword("CRYPTO") == "CRYPTOABDEFGHIJKLMNQSUVWXZ"
    assert monoalpha.encrypt("HELLO", KEY) == "ACGGK"
    assert monoalpha.encrypt("BOB", KEY) == "NKN"


def test_roundtrip():
    plaintext = "HELLOWORLD"
    assert monoalpha.decrypt(monoalpha.encrypt(plaintext, KEY), KEY) == plaintext


def test_rejects_key_with_wrong_length():
    with pytest.raises(ValueError):
        monoalpha.encrypt("abc", "TOOSHORT")


def test_rejects_key_with_repeated_letters():
    bad_key = "AABCDEFGHIJKLMNOPQRSTUVWXY"
    with pytest.raises(ValueError):
        monoalpha.encrypt("abc", bad_key)


def test_key_from_keyword_keeps_full_alphabet():
    key = monoalpha.key_from_keyword("PYTHON")
    assert len(key) == 26
    assert sorted(key) == sorted("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def test_key_from_keyword_ignores_repeated_letters_in_keyword():
    assert monoalpha.key_from_keyword("BANANA")[:3] == "BAN"



def test_empty_input():
    assert monoalpha.encrypt("", KEY) == ""


def test_single_character():
    assert monoalpha.decrypt(monoalpha.encrypt("A", KEY), KEY) == "A"


def test_input_with_no_letters():
    assert monoalpha.encrypt("12345 !!! ,,,", KEY) == ""