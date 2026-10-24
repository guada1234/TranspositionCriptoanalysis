import pytest

import affine


def test_check_value_from_handout():
    assert affine.encrypt("attack", 5, 8) == "IZZISG"


def test_roundtrip():
    plaintext = "HELLOWORLD"
    assert affine.decrypt(affine.encrypt(plaintext, 5, 8), 5, 8) == plaintext
    assert affine.decrypt(affine.encrypt(plaintext, 7, 3), 7, 3) == plaintext


def test_valid_keys_size():
    keys = affine.valid_keys()
    assert len(keys) == 312


def test_valid_keys_only_contains_coprime_a():
    valid_a_values = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}
    for (a, b) in affine.valid_keys():
        assert a in valid_a_values
        assert 0 <= b <= 25


def test_rejects_non_coprime_a():
    with pytest.raises(ValueError):
        affine.encrypt("abc", 13, 0)
    with pytest.raises(ValueError):
        affine.encrypt("abc", 2, 0)
    with pytest.raises(ValueError):
        affine.decrypt("abc", 4, 0)


def test_roundtrip_for_every_valid_key():
    plaintext = "THEQUICKBROWNFOX"
    for (a, b) in affine.valid_keys():
        ciphertext = affine.encrypt(plaintext, a, b)
        assert affine.decrypt(ciphertext, a, b) == plaintext


def test_empty_input():
    assert affine.encrypt("", 5, 8) == ""


def test_single_character():
    assert affine.decrypt(affine.encrypt("A", 5, 8), 5, 8) == "A"


def test_input_with_no_letters():
    assert affine.encrypt("12345 !!! ,,,", 5, 8) == ""