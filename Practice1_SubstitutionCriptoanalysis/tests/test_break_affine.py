import random
import pytest

import affine
from break_affine import break_affine
from tests.reference_texts import REFERENCE_TEXT_EN, REFERENCE_TEXT_ES

def test_break_affine_recovers_a_known_key_english():
    fragment = REFERENCE_TEXT_EN[:180]
    ciphertext = affine.encrypt(fragment, 7, 3)

    key, plaintext = break_affine(ciphertext, "en")
    assert key == (7, 3)
    assert plaintext == fragment


def test_break_affine_recovers_a_known_key_spanish():
    fragment = REFERENCE_TEXT_ES[:180]
    ciphertext = affine.encrypt(fragment, 5, 8)

    key, plaintext = break_affine(ciphertext, "es")
    assert key == (5, 8)
    assert plaintext == fragment


def test_break_affine_identity_key_is_found_correctly():
    # a=1, b=0 means "encrypt" did nothing at all
    fragment = REFERENCE_TEXT_EN[:180]
    key, plaintext = break_affine(fragment, "en")
    assert key == (1, 0)
    assert plaintext == fragment


def test_break_affine_rejects_unknown_language():
    with pytest.raises(ValueError):
        break_affine("ABCDEF", "fr")


def test_break_affine_only_returns_valid_keys():
    # the winning key must always be one of the 312 valid (a, b) pairs
    fragment = REFERENCE_TEXT_EN[:180]
    ciphertext = affine.encrypt(fragment, 11, 15)

    key, plaintext = break_affine(ciphertext, "en")
    assert key in affine.valid_keys()


FRAGMENT_LENGTH = 150
TRIALS = 20


def test_break_affine_recovers_key_reliably():
    random.seed(3)
    valid_keys = affine.valid_keys()
    last_start = len(REFERENCE_TEXT_EN) - FRAGMENT_LENGTH

    successes = 0
    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_EN[start:start + FRAGMENT_LENGTH]

        a, b = random.choice(valid_keys)
        ciphertext = affine.encrypt(fragment, a, b)

        found_key, found_plaintext = break_affine(ciphertext, "en")
        if found_key == (a, b):
            successes = successes + 1

    assert successes == TRIALS