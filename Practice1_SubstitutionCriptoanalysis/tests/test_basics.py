import pytest
import basics


def test_to_numbers_basic():
    assert basics.to_numbers("ABC") == [0, 1, 2]


def test_to_numbers_drops_non_letters_and_uppercases():
    assert basics.to_numbers("Hello, World! 123") == basics.to_numbers("HELLOWORLD")


def test_to_letters_basic():
    assert basics.to_letters([0, 1, 2]) == "ABC"


def test_to_letters_wraps_negative_and_large_numbers():
    assert basics.to_letters([-1, 26, 27]) == "ZAB"


def test_roundtrip_numbers_and_letters():
    text = "THEQUICKBROWNFOX"
    assert basics.to_letters(basics.to_numbers(text)) == text

def test_modinv_check_values():
    assert basics.modinv(5, 26) == 21
    assert basics.modinv(7, 26) == 15
    assert basics.modinv(17, 26) == 23


def test_modinv_rejects_non_coprime_values():
    with pytest.raises(ValueError):
        basics.modinv(13, 26)
    with pytest.raises(ValueError):
        basics.modinv(2, 26)


def test_modinv_actually_inverts():
    # a * modinv(a, 26) should be 1, modulo 26, for every valid a
    for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
        inverse = basics.modinv(a, 26)
        assert (a * inverse) % 26 == 1


def test_egcd_basic():
    g, x, y = basics.egcd(30, 18)
    assert g == 6
    assert 30 * x + 18 * y == g


def test_egcd_with_negative_inputs():
    g, x, y = basics.egcd(-3, 7)
    assert g == 1
    assert -3 * x + 7 * y == g


def test_xor_bytes_check_value():
    assert basics.xor_bytes(b"HELLO", b"KEYKE").hex() == "030015070a"


def test_xor_bytes_is_its_own_inverse():
    data = b"HELLO WORLD, THIS IS A TEST"
    key = b"KEY"
    assert basics.xor_bytes(basics.xor_bytes(data, key), key) == data


def test_xor_bytes_key_repeats_cyclically():
    # key shorter than data must wrap around
    assert basics.xor_bytes(b"AAAA", b"A") == bytes([0, 0, 0, 0])