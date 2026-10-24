import random
import caesar
from break_caesar import break_caesar
from tests.reference_texts import REFERENCE_TEXT_EN, REFERENCE_TEXT_ES

LENGTHS = [20, 30, 40, 60, 100]
TRIALS = 200


def recovery_rate(reference_text: str, language: str, seed: int) -> dict[int, float]:
    random.seed(seed)
    rates = {}

    for length in LENGTHS:
        last_start = len(reference_text) - length
        successes = 0

        for trial in range(TRIALS):
            start = random.randint(0, last_start)
            fragment = reference_text[start:start + length]

            key = random.randint(0, 25)
            ciphertext = caesar.encrypt(fragment, key)

            found_key, found_plaintext = break_caesar(ciphertext, language)
            if found_key == key:
                successes = successes + 1

        rates[length] = (successes / TRIALS) * 100

    return rates


def print_row(label: str, rates: dict[int, float]) -> None:
    cells = []
    for length in LENGTHS:
        cells.append(f"{rates[length]:5.1f}%")
    print(f"{label:35s}" + "  ".join(cells))


def main() -> None:
    print("Lengths:                          " + "     ".join(f"{n:3d}" for n in LENGTHS))
    print("-" * 80)

    rates_en_en = recovery_rate(REFERENCE_TEXT_EN, "en", seed=101)
    print_row("English text, English table:", rates_en_en)

    rates_es_en = recovery_rate(REFERENCE_TEXT_ES, "en", seed=102)
    print_row("Spanish text, English table (WRONG):", rates_es_en)

    rates_es_es = recovery_rate(REFERENCE_TEXT_ES, "es", seed=103)
    print_row("Spanish text, Spanish table:", rates_es_es)


if __name__ == "__main__":
    main()