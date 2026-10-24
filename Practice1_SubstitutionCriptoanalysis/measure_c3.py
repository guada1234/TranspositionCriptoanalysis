import random
import vigenere
from break_vigenere import break_vigenere
from tests.reference_texts import REFERENCE_TEXT_EN

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEY_LENGTHS = [3, 5, 7]
TOTAL_LENGTHS = [60, 120, 200, 300]
TRIALS = 100


def _random_key(length: int) -> str:
    letters = []
    for i in range(length):
        letters.append(random.choice(ALPHABET))
    return "".join(letters)


def recovery_rate(key_length: int, total_length: int, seed: int) -> float:
    random.seed(seed)
    last_start = len(REFERENCE_TEXT_EN) - total_length
    successes = 0

    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_EN[start:start + total_length]

        key = _random_key(key_length)
        ciphertext = vigenere.encrypt(fragment, key)

        found_key, found_plaintext = break_vigenere(ciphertext, key_length, "en")
        if found_key == key:
            successes = successes + 1

    return (successes / TRIALS) * 100


def main() -> None:
    header = "key length \\ total length   " + "   ".join(f"{n:5d}" for n in TOTAL_LENGTHS)
    print(header)
    print("-" * len(header))

    seed = 200
    for m in KEY_LENGTHS:
        cells = []
        for total_length in TOTAL_LENGTHS:
            seed = seed + 1
            rate = recovery_rate(m, total_length, seed)
            cells.append(f"{rate:5.1f}%")
        print(f"m = {m:<24d}" + "  ".join(cells))


if __name__ == "__main__":
    main()