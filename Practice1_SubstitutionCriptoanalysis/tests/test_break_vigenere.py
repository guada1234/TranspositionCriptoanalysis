import random
import pytest
import vigenere
from break_vigenere import break_vigenere
from tests.reference_texts import REFERENCE_TEXT_EN

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _random_key(length: int) -> str:
    letters = []
    for i in range(length):
        letters.append(random.choice(ALPHABET))
    return "".join(letters)


def test_break_vigenere_recovers_a_known_key():
    fragment = REFERENCE_TEXT_EN[:300]
    ciphertext = vigenere.encrypt(fragment, "LEMON")

    key, plaintext = break_vigenere(ciphertext, 5, "en")
    assert key == "LEMON"
    assert plaintext == fragment


def test_break_vigenere_key_length_one_behaves_like_caesar():
    import caesar
    fragment = REFERENCE_TEXT_EN[:150]
    ciphertext = vigenere.encrypt(fragment, "D")

    key, plaintext = break_vigenere(ciphertext, 1, "en")
    assert key == "D"
    assert plaintext == fragment
    # sanity check: also matches the plain Caesar breaker
    assert plaintext == caesar.decrypt(ciphertext, 3)


def test_break_vigenere_returned_key_has_length_m():
    fragment = REFERENCE_TEXT_EN[:300]
    ciphertext = vigenere.encrypt(fragment, "SECRET")

    key, plaintext = break_vigenere(ciphertext, 6, "en")
    assert len(key) == 6


def test_break_vigenere_rejects_unknown_language():
    with pytest.raises(ValueError):
        break_vigenere("ABCDEFGHIJ", 3, "fr")


def test_break_vigenere_with_wrong_m_gives_no_warning():
    fragment = REFERENCE_TEXT_EN[:300]
    ciphertext = vigenere.encrypt(fragment, "LEMON")   # true key length is 5

    wrong_key, wrong_plaintext = break_vigenere(ciphertext, 4, "en")   # wrong m on purpose

    assert len(wrong_key) == 4
    assert wrong_plaintext != fragment 


KEY_LENGTH = 5
TOTAL_LENGTH = 300
TRIALS = 20


def test_break_vigenere_recovers_key_reliably():
    random.seed(4)
    last_start = len(REFERENCE_TEXT_EN) - TOTAL_LENGTH

    successes = 0
    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_EN[start:start + TOTAL_LENGTH]

        key = _random_key(KEY_LENGTH)
        ciphertext = vigenere.encrypt(fragment, key)

        found_key, found_plaintext = break_vigenere(ciphertext, KEY_LENGTH, "en")
        if found_key == key:
            successes = successes + 1

    assert successes == TRIALS