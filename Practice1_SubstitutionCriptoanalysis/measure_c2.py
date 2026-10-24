import random
import affine
from break_affine import break_affine
from tests.reference_texts import REFERENCE_TEXT_EN

LENGTHS = [20, 30, 40, 60, 100]
TRIALS = 200


def recovery_rate(length: int, seed: int) -> float:
    random.seed(seed)
    valid_keys = affine.valid_keys()
    last_start = len(REFERENCE_TEXT_EN) - length
    successes = 0

    for trial in range(TRIALS):
        start = random.randint(0, last_start)
        fragment = REFERENCE_TEXT_EN[start:start + length]

        a, b = random.choice(valid_keys)
        ciphertext = affine.encrypt(fragment, a, b)

        found_key, found_plaintext = break_affine(ciphertext, "en")
        if found_key == (a, b):
            successes = successes + 1

    return (successes / TRIALS) * 100


def main() -> None:
    print("Lengths:            " + "     ".join(f"{n:3d}" for n in LENGTHS))
    print("-" * 60)
    cells = []
    seed = 300
    for length in LENGTHS:
        seed = seed + 1
        rate = recovery_rate(length, seed)
        cells.append(f"{rate:5.1f}%")
    print("English text:       " + "  ".join(cells))


if __name__ == "__main__":
    main()