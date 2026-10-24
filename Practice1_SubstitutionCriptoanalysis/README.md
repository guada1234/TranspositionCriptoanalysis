# Practice 1 — Substitution Ciphers and Their Cryptanalysis

**Author:** Guadalupe Rial


**Course:**  Cryptography · Bachelor in Data Science and Engineering · Universidad CEU San Pablo · Academic year 2026/27

---

## 1. How to run everything

All commands assume you are in the project root.

Install the only optional dependency (needed for the test suite):

```bash
pip install pytest
```

Run the full test suite:

```bash
pytest -v
```

Run the measurement scripts (Parts C1, C2, C3) and reproduce the
tables in this report:

```bash
python measure_c1.py
python measure_c2.py
python measure_c3.py
```

Command-line interface (Part D), a few examples — see Part D of the
handout for the full list:

```bash
python crypto.py caesar encrypt --key 3 --in message.txt
python crypto.py affine decrypt --a 5 --b 8 --in cipher.txt --out plain.txt
python crypto.py mono encrypt --keyword CRYPTO --in message.txt
python crypto.py vigenere encrypt --key LEMON --in message.txt
python crypto.py break caesar --in cipher.txt --lang es
python crypto.py break affine --in cipher.txt
python crypto.py break vigenere --m 5 --in cipher.txt
python crypto.py assist --in cipher.txt
```

If `--in` is omitted, the program reads from standard input; if
`--out` is omitted, it writes to standard output.

---

## 2. Key space size for each cipher

| Cipher | Key space | Reasoning |
|---|---|---|
| Caesar | 26 | The key is a single shift `k` in `0..25`. |
| Affine | 312 | `E(x) = a*x + b`. `a` must be coprime (mcd(a,26) = 1) with 26 (12 valid values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25), `b` can be any of the 26 values. `12 * 26 = 312`. |
| Monoalphabetic substitution | 26! ≈ 4.03 × 10²⁶ | The key is any permutation of the 26 letter alphabet; there are `26!` distinct permutations. |
| Vigenère (key length `m`, fixed) | 26^m | Each of the `m` key positions is independently any of the 26 letters. (If `m` itself is unknown, the space is technically unbounded, since any key length is allowed, but for a *given* `m`, it is `26^m`.) |

---

## 3. Part C1 — Caesar breaker, measurement

**Frequency tables used, and their source.** `break_caesar.py` ships
one dictionary per language, `ENGLISH_FREQUENCIES` and
`SPANISH_FREQUENCIES`, each mapping a letter to its expected
percentage. Both tables are the standard letter frequency figures
commonly reported on Wikipedia's "Letter frequency" article: the
English values trace back to Lewand's *Cryptological Mathematics*
(the classic E=12.702%, T=9.056%, A=8.167%... table used in most
cryptography courses), and the Spanish values are based on a Real
Academia Española corpus. I removed 'Ñ' from the Spanish table since
it is not part of my 26-letter A-Z alphabet. `break_caesar` picks the
right table with a simple `if language == "en" / "es"` check, and
raises `ValueError` for any other language string.

Ran with `python measure_c1.py` (200 trials per cell, `random.seed`
fixed per row for reproducibility):

| Length | English text / English table | Spanish text / English table (WRONG) | Spanish text / Spanish table |
|---:|---:|---:|---:|
| 20  | 92.5%  | 82.0%  | 100.0% |
| 30  | 95.5%  | 91.5%  | 100.0% |
| 40  | 100.0% | 96.5%  | 100.0% |
| 60  | 100.0% | 100.0% | 100.0% |
| 100 | 100.0% | 100.0% | 100.0% |

**At which length does the breaker become reliable?**
Looking at the table, the breaker already works pretty well at 20 letters (92.5%–100%), and by 40 letters it's basically perfect (100%) in both languages. Below 30 letters is where it occasionally messes up. I think this happens because with so few letters, the count of each letter can look "off" just by chance, so sometimes a wrong shift ends up looking more normal to chi_squared than the actual correct one.

**How much does the wrong language table actually cost you?**
Less than I expected, honestly. Using the English table on Spanish text only drops the accuracy by about 10–18 points at the short lengths (82.0% vs 100.0% at 20 letters, 91.5% vs 100.0% at 30 letters), and by 40 letters there's basically no difference anymore. My guess is that English and Spanish aren't that different when it comes to which letters show up the most (E, A, O and a couple of consonants dominate in both), so even with the "wrong" table, chi_squared still tends to point in the right direction most of the time.

---

## 4. Part C2 — Affine breaker, measurement and comparison with C1

Ran with `python measure_c2.py` (200 trials per cell, English text):

| Length | Affine (312 keys tried) | Caesar (26 keys tried, from C1) |
|---:|---:|---:|
| 20  | 74.5%  | 92.5%  |
| 30  | 88.5%  | 95.5%  |
| 40  | 96.0%  | 100.0% |
| 60  | 99.5%  | 100.0% |
| 100 | 100.0% | 100.0% |

I tested **312 candidates** for affine, because that is exactly
`len(affine.valid_keys())` — every `(a, b)` pair with `a` coprime with
26 — the true size of the affine key space, not an arbitrary choice.

**Comparison with C1:** affine needs a bit more ciphertext than Caesar to be just as reliable (74.5% vs 92.5% at 20 letters, 96.0% vs 100.0% at 40 letters). This makes sense to me: affine has 12 times more candidate keys than Caesar (312 vs 26), so there are just more chances for a wrong (a, b) pair to get lucky and produce a decryption that looks slightly more "normal" than the real one, especially on short, noisy fragments where the letter counts aren't very stable yet.

---

## 5. Part C3 — Vigenère breaker, measurement

Ran with `python measure_c3.py` (100 trials per cell, English text):

| Key length `m` | Total = 60 (≈letters/coset) | Total = 120 | Total = 200 | Total = 300 |
|---|---:|---:|---:|---:|
| m = 3 (20/40/67/100 per coset) | 71.0%  | 100.0% | 100.0% | 100.0% |
| m = 5 (12/24/40/60 per coset)  | 29.0%  | 83.0%  | 100.0% | 100.0% |
| m = 7 (~9/17/29/43 per coset)  | 6.0%   | 27.0%  | 100.0% | 100.0% |

**What actually governs whether this works — total ciphertext length,
or something else?**
It's not really the total length, it's how many letters end up in each coset, basically total_length / m. You can see it clearly in the table: with a total length of 60, m=3 gives each coset 20 letters and works 71% of the time, but m=7 gives each coset only 9 letters and works just 6% of the time — same amount of ciphertext, completely different results. That's because each coset gets broken separately with break_caesar, so what matters is how many letters that coset has, not how long the whole message is.

**Why does a longer key make Vigenère stronger, even though the
cipher itself hasn't changed?**  If you keep the total ciphertext length fixed, a longer key m means the letters get split into more cosets, so each one ends up with fewer letters. And from C1 I already saw that break_caesar needs a minimum amount of letters per coset to work reliably. So the cipher itself isn't doing anything different — a longer key just means the attacker has less data to work with in each coset, and that's exactly what makes it harder to break.

---

## 6. Part C4 — Frequency assistant, findings on the given cryptogram

Ran with python -c "import assist; print(assist.report(open('cryptogram.txt').read(), 'en'))" on the 110-letter, 22-distinct-letter cryptogram from the handout.
How I solved it, step by step, using only the report and finishing it by hand:

1. T sits at 18.18% in the frequency table — far ahead of everything else — so T→E from the start.
2. The repeated-trigram list is the most useful part of the report: QAT appears 3 times, at three unrelated positions. Three independent repeats of the same chunk is a strong signal, and THE is the most common English trigram, so I tried Q→T, A→H, T→E. Decoding produced "THE" correctly at all three spots.
3. My first idea for what follows the opening "THE" was "THERE" (N→R), since NT is a frequent bigram (4 occurrences) and THERE is a very common word. This looked right locally, but decoding further into the message with N→R produced broken fragments later on, so I abandoned it. 
4. Since this cryptogram is clearly about cryptography itself, I tried topic-relevant words instead of generic ones. Right after "THE", I tried "SECURITY" — and it fit perfectly: the two ciphertext letters already fixed (T→E, Q→T) landed exactly where SECURITY's own E and T need to be, which confirmed the guess and handed me six new letters at once (N→S, Y→C, S→U, M→R, H→I, X→Y).
5. From there it became a chain reaction: decoding with each new batch of letters revealed enough of the next word to guess it, and each guess was checked against everything decoded so far, not just the spot where it was made:
    "OF A CIPHER" → J→O, O→F, C→A, K→P
    "MUST" and the very last word, which was unmistakably "COMPROMISED" → F→M, P→D
    "NEVER" and "DEPEND" → I→N, U→V
    "ON KEEPING" → D→K, and G→G (a letter that happens to map to itself — perfectly valid in a permutation)
    "THE ALGORITHM" and "SECRET" → E→L
    "BECAUSE" → R→B
    "ONLY THE KEY CAN BE CHANGED WHEN IT IS" fell out of letters already known, except V→W for "WHEN"
6. That resolves all 22 ciphertext letters that actually appear in the message, and decrypting the whole thing with the final key reproduces, with no leftover unmapped letters:
THE SECURITY OF A CIPHER MUST NEVER DEPEND ON KEEPING THE ALGORITHM SECRET, BECAUSE ONLY THE KEY CAN BE CHANGED WHEN IT IS COMPROMISED.

**How many of the 22 distinct letters did the suggested mapping (rank alignment alone) get right?** Comparing assist.py's suggested mapping against the key I actually solved for, only 3 out of 22 distinct ciphertext letters were correct: H→I, T→E, and U→V. T→E, the single most useful line, since T is overwhelmingly the most frequent ciphertext letter, was indeed correct, but almost everything else was wrong, including letters that are individually common in English (e.g. it suggested A→O when the real mapping is A→H).

**Why rank alignment alone doesn't solve the cipher, and what does.** With only 110 letters, the middle of the frequency ranking is statistically noisy, several ciphertext letters have nearly identical counts, so their relative order is mostly decided by chance rather than by a genuine frequency difference. Only the most extreme entries in the ranking (the very top, like T, and letters that don't appear at all) carry a strong enough signal to trust directly. What actually solves the cipher is combining that reliable top-of-the-ranking guess with structural evidence, repeated trigrams that must correspond to common chunks like THE, and then, crucially, guessing whole words that fit the topic of the message and checking each guess against the entire decoded text so far, backtracking whenever a locally-plausible guess (like my N→R "THERE" attempt) turns out to break somewhere else.

---

## 7. Why 26! resists a computer, but not a human with a frequency table

A monoalphabetic substitution has a key space of 26! ≈ 4 × 10²⁶, which is actually bigger than an 88 bit brute force space, so no computer is going to try every single key one by one. But that's not how you actually break it, the trick is that normal language has a very predictable letter/bigram/trigram distribution (it has structure), and that leaks a ton of information about each letter of the key almost independently of the rest. So instead of guessing one out of 26! possibilities, it's more like guessing one out of 26 options, 26 separate times, each time with frequency and word pattern clues to help, which is something a person can actually do with pen and paper. AES-128 is built specifically so this can't happen: because of its S-boxes and multiple rounds, changing a single bit of input scrambles about half the output bits, so the ciphertext ends up looking completely random no matter which key was used. There's no letter-by-letter leak to exploit like with substitution ciphers, so the only real way to attack it is to try to exhaust the key space, which is exactly why AES-128 stays secure even though, on paper, its key space is much smaller than 26!.

---

## 8. Limitations / what does not work

`break_caesar` / `break_affine` can return a wrong key on very short
  or unusual fragments.

**Observation during CLI testing (relevant to C1/C2 reliability).**
While testing `crypto.py`, I first validated the `break caesar` and
`break affine` commands using a short test message (`"MySecretMessage"`,
15 letters). Both commands returned an incorrect key on this input.
Before treating this as a bug, I re-ran the same test with a longer,
more natural English text (around 175 letters) encrypted with the same
ciphers. With the longer text, both `break caesar` and `break affine`
recovered the exact key and the exact plaintext. This confirms that
the failure on the 15 letter message was not a defect in the
implementation, but an instance of the exact phenomenon Part C1 asks
me to measure: for very short ciphertexts, the chi-squared statistic
does not have enough letters to reliably distinguish the correct key
from a wrong one. This is consistent with my C1 measurement results
above, where reliability only becomes consistent above a certain
minimum length. I kept this as a documented, expected limitation
rather than a bug to fix.


**`break_vigenere` doesn't check if `m` is actually right.** I noticed this while testing: if you give it the wrong key length, it doesn't crash or throw a warning or anything, it just goes ahead and gives you back *a* key and *a* "decrypted" text like everything's fine, even though it's total garbage. I actually wrote a test for this (`test_break_vigenere_with_wrong_m_gives_no_warning`): I encrypt something with a 5-letter key, then call `break_vigenere` telling it the key is 4 letters on purpose, and yeah, it just returns a 4-letter key and nonsense text, no errors at all. Makes sense though, since figuring out `m` on your own is apparently a whole other topic, so I guess for now it's on the person using the function to actually look at the output and notice if it doesn't look like real English or not.

---

## LLM assistance declaration

I used Claude as an assistant throughout Parts A-D, always asking it to
explain the reasoning behind a piece of code before accepting it, so
that I could reproduce and justify every line myself.

- **`basics.py` (Part A).** This is where I relied on it the most,
  because I didn't initially know Python had `ord()`/`chr()` for
  converting between a character and its code point. My first working
  version of `to_numbers`/`to_letters` used a hardcoded string
  `ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"` and looked up each letter's
  position with `ALPHABET.index(letter)` / `ALPHABET[n]`. It worked,
  but felt clunky, especially for `to_letters`, where I had to write
  `n % 26` before indexing to avoid crashing on out-of-range numbers.
  After asking Claude to explain a simpler way, I switched to the
  `ord("A")` / `chr(...)` version that's in the final file, which
  avoids carrying the alphabet string around everywhere.
- **`caesar.py`, `affine.py`, `monoalpha.py`, `vigenere.py` (Part B).**
  Used it to check my understanding of the modular arithmetic (why
  `to_letters` needs the `% 26` and the cipher formulas don't).
- **`break_caesar.py`, `break_affine.py`, `break_vigenere.py`, `assist.py` (Part C).**
  Asked for help designing the chi-squared scoring function and
  understanding why it has to be normalised by text length, and for
  help structuring `assist.py`'s report sections (letter frequencies,
  n-grams, doubled letters, mapping suggestion).
- **`tests/` (Section 3).** Used it to help scaffold the pytest suite
  structure (`conftest.py` for import paths, the `reference_texts.py`
  helper module, the pattern for the 20-trial reliability tests with a
  fixed `random.seed`), which I then adapted and re-ran myself to
  confirm the numbers.
- **tests/reference_texts.py**. This whole file was written by Claude, not adapted from something I wrote, it's two short paragraphs (English and Spanish) about cryptography, composed specifically for this practice (not copied from any external source), normalized with to_numbers/to_letters. I use it as the "natural language" source in the breaker tests: test_break_caesar.py, test_break_affine.py and test_break_vigenere.py all take random fragments from these two paragraphs, encrypt them with a random key, and check whether the breaker recovers that key, this is what lets those tests be reproducible (with random.seed) while still using text with a realistic letter distribution instead of made-up strings.
- **`measure_c1.py`, `measure_c2.py`, `measure_c3.py`.** Used it to
  help write these measurement scripts and to draft the first version
  of this README's tables and analysis text, all of which I then ran
  myself, checked against the actual output, and edited into my
  own words where needed.
- **`crypto.py` (Part D).** Used it to help design the `argparse`
  subcommand structure (one subparser per cipher, plus `break` and
  `assist`), since I hadn't used `argparse` subparsers before, and to
  get the try/except wrapper right so no raw traceback reaches the
  user.
- **This README's wording.** I asked Claude to rephrase my
  own draft sentences into more precise, academic, and formal wording
  (correct terminology, more formal register) without changing what I
  was actually saying.