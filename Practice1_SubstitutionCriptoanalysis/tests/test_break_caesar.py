import random
import pytest
import caesar
from break_caesar import chi_squared, break_caesar, ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES
from tests.reference_texts import REFERENCE_TEXT_EN, REFERENCE_TEXT_ES

def test_chi_squared_of_empty_text_is_zero():
    assert chi_squared("", ENGLISH_FREQUENCIES) == 0.0


def test_chi_squared_is_lower_for_the_matching_language():
    # a real English text should score better (lower) against the
    # English table than against the Spanish table
    score_en = chi_squared(REFERENCE_TEXT_EN, ENGLISH_FREQUENCIES)
    score_es = chi_squared(REFERENCE_TEXT_EN, SPANISH_FREQUENCIES)
    assert score_en < score_es


def test_chi_squared_is_lower_for_correct_shift_than_wrong_shift():
    # decrypting with the correct key should look more "normal" than
    # decrypting with a wrong key
    fragment = REFERENCE_TEXT_EN[:120]
    ciphertext = caesar.encrypt(fragment, 11)

    correct_candidate = caesar.decrypt(ciphertext, 11)
    wrong_candidate = caesar.decrypt(ciphertext, 5)

    score_correct = chi_squared(correct_candidate, ENGLISH_FREQUENCIES)
    score_wrong = chi_squared(wrong_candidate, ENGLISH_FREQUENCIES)
    assert score_correct < score_wrong


def test_break_caesar_recovers_a_known_key_english():
    fragment = REFERENCE_TEXT_EN[:150]
    ciphertext = caesar.encrypt(fragment, 11)

    key, plaintext = break_caesar(ciphertext, "en")
    assert key == 11
    assert plaintext == fragment


def test_break_caesar_recovers_a_known_key_spanish():
    fragment = REFERENCE_TEXT_ES[:150]
    ciphertext = caesar.encrypt(fragment, 7)

    key, plaintext = break_caesar(ciphertext, "es")
    assert key == 7
    assert plaintext == fragment


def test_break_caesar_rejects_unknown_language():
    with pytest.raises(ValueError):
        break_caesar("ABCDEF", "fr")


def test_break_caesar_shift_zero_is_found_correctly():
    # a shift of 0 means "encrypt" did nothing at all; make sure the
    # breaker doesn't get confused by this edge case
    fragment = REFERENCE_TEXT_EN[:150]
    key, plaintext = break_caesar(fragment, "en")
    assert key == 0
    assert plaintext == fragment


FRAGMENT_LENGTH = 150
TRIALS = 20


def test_break_caesar_recovers_key_reliably_english():
    random.seed(1)
    last_start = len(REFERENCE_TEXT_EN) - FRAGMENT_LENGTH

    successes = 0
    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_EN[start:start + FRAGMENT_LENGTH]

        key = random.randint(0, 25)
        ciphertext = caesar.encrypt(fragment, key)

        found_key, found_plaintext = break_caesar(ciphertext, "en")
        if found_key == key:
            successes = successes + 1

    assert successes == TRIALS


def test_break_caesar_recovers_key_reliably_spanish():
    random.seed(2)
    last_start = len(REFERENCE_TEXT_ES) - FRAGMENT_LENGTH

    successes = 0
    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_ES[start:start + FRAGMENT_LENGTH]

        key = random.randint(0, 25)
        ciphertext = caesar.encrypt(fragment, key)

        found_key, found_plaintext = break_caesar(ciphertext, "es")
        if found_key == key:
            successes = successes + 1

    assert successes == TRIALS