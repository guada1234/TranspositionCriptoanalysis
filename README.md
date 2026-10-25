# Practice 2: Transposition Ciphers and Classical Cryptanalysis

**20357 Cryptography** · Bachelor in Data Science and Engineering · Universidad CEU San Pablo · Academic year 2026/27

Guadalupe Rial · Individual submission (no pair)

---

## 1. How to run everything

All commands are run from the main project folder. Only the Python standard library (3.11 or later) is used, plus `pytest` for the tests.

### Structure

```
railfence.py  columnar.py  measure.py  kasiski.py  keylength.py
break_vigenere.py  break_columnar.py  attack.py  crypto.py
referencia.txt                       ← reference text (Pride and Prejudice, ch. 1–4)
Practice1_SubstitutionCriptoanalysis/  ← Practice 1 modules that are imported
tests/
```

### Tests

```
python3 -m pytest tests
```

### Report measurements

Each of these programs repeats one of the measurements in the report and prints its tables. They all use a fixed random seed, so they always give the same numbers.

- `python3 measure.py` — B1 and B2. First, for texts from 10 to 400 letters, it computes the index of coincidence of 200 fragments of the reference text and shows what percentage looks more like English than like random letters. This gives the minimum length from which the IC is reliable. Then it generates 150 transpositions and 150 substitutions of each length (60, 120, 250 and 400 letters), chooses the classifier threshold that makes the fewest mistakes, and shows the error rate for each length. It does this twice: with X padding and with random padding.
- `python3 keylength.py` — C1. First it calibrates the threshold of find_key_length: it encrypts 200 texts with Vigenère using keys of known length, and shows how many times the length is found with each fraction (from 0.5 to 0.9). Then it encrypts a text with the key CIPHER and shows the coset_ic table for m = 1 to 16, marking the true length, its multiples and its divisors.
- `python3 break_vigenere.py` — C2. It attacks 2,000 texts encrypted with Vigenère: 100 for each combination of key length (3, 5, 7 and 9) and text length (100, 150, 200, 300 and 400 letters), without telling the attack the key length. It prints two tables: in how many cases it recovers the complete key, and in how many it finds only the key length.
- `python3 break_columnar.py` — C3. It attacks 1,200 texts encrypted by columns: 100 for each combination of number of columns (4, 5, 6 and 7) and text length (60, 120 and 200 letters), and shows in what percentage it recovers the exact text. Then it measures how long the attack takes with 7, 8 and 9 columns, to find the largest number solved in under 10 seconds.


### Automatic attack (Part D)

```
python3 attack.py --in cipher.txt
python3 attack.py --in cipher.txt --lang es
python3 attack.py --in cipher.txt --cols 6
```

### "Extended" command line from Practice 1

```
python3 crypto.py railfence encrypt --rails 3     --in message.txt
python3 crypto.py railfence decrypt --rails 3     --in cipher.txt
python3 crypto.py columnar  encrypt --key CIPHER  --in message.txt
python3 crypto.py columnar  decrypt --key CIPHER  --in cipher.txt
python3 crypto.py measure   ic                    --in cipher.txt
python3 crypto.py measure   classify              --in cipher.txt
python3 crypto.py measure   kasiski               --in cipher.txt
```

The Practice 1 commands (`caesar`, `affine`, `mono`, `vigenere`, `break`, `assist`) still work the same way.

### Reference text

Pride and Prejudice, by Jane Austen (Project Gutenberg #1342).
Chapters 1 to 4, without images or chapter titles. 
Downloaded from: https://www.gutenberg.org/cache/epub/1342/pg1342.txt

---

## 2. A3: Double transposition and padding

Double transposition encrypts twice in a row: first with `kw1` and then, on the result, with `kw2`. To decrypt, it is done the other way round: first `kw2` is undone and then `kw1`.

**My first version.** At first, `encrypt_double` simply called `encrypt` twice, and `decrypt_double` called `decrypt` twice. It worked with the example in the handout, but only by chance: the text has 30 letters, and 30 is a multiple of 5 (`ROTOR`) and of 6 (`ENIGMA`), so neither pass needed padding.

When I tested it with a 32-letter text and the keys `ABC` (3 columns) and `ABCDEF` (6 columns), it failed:

- Original text: `THESAMEKEYMUSTNEVERBEUSEDTWICEAB`
- Result of encrypting and decrypting: `TAESKUEMNYTESVEEBERSWUTEDCXIBXAEXHMX`

All the letters are there, but in the wrong order. And no error appeared: the function returned the wrongly decrypted text without any warning.

**Why it fails.** `encrypt` pads with X until the text fills its matrix, that is, up to a multiple of the number of columns. When encrypting twice, it pads twice:

- **Pass 1** (3 columns): 32 letters → 1 X is added → **33 letters**, in a matrix of 11 rows.
- **Pass 2** (6 columns): 33 letters → 3 X are added → **36 letters**.

When decrypting, the first step undoes pass 2 and returns 36 letters. The second step should receive the 33 letters that came out of pass 1, but it receives 36, because nobody removed the 3 X added by pass 2. `decrypt_double` cannot remove them: it does not know how many letters the original text had, so it does not know how many of those X are padding (and some could be part of the message).

With 36 letters and 3 columns, `decrypt` thinks the matrix has 12 rows, when during encryption it had 11. So it takes the letters 12 at a time instead of 11 at a time: the first column takes a letter that does not belong to it, and the shift carries over to all the others. Since 36 is also a multiple of 3, `decrypt` sees nothing unusual and raises no error.

**My solution.** `encrypt_double` pads only once, at the beginning, up to a multiple of both key lengths at the same time. The smallest number that is a multiple of both is the least common multiple:

- `math.lcm(3, 6)` = 6, so the 32 letters are padded to 36.
- **Pass 1:** 36 is already a multiple of 3 → nothing is added.
- **Pass 2:** 36 is already a multiple of 6 → nothing is added.

Since neither pass adds its own padding, when decrypting each step receives exactly the letters it needs. Now the same example returns:

`THESAMEKEYMUSTNEVERBEUSEDTWICEABXXXX`

This is the original text plus the 4 X of padding added at the beginning.

That is why `decrypt_double` does not need to do anything special: the problem is avoided when encrypting, and when decrypting it only has to undo the two passes in reverse order (first `kw2`, then `kw1`).

Nothing changes with the example in the handout: 30 is already a multiple of 5 and 6, so no padding is added and the result is still `WCTEIHSTAEVREBEUTMNSUEEDSEEMYK`.

---

## 3. B1: From what length is the index of coincidence reliable?

`CRYPTANALYSIS` is an English word and its IC is 0.0385, the same as that of random letters (1/26). With only 13 letters, the result depends on chance: one letter repeated more or less changes the value a lot.

**How I decided.** For each length, I took 200 random fragments of the reference text and computed their IC. Then I counted how many are closer to English (0.0655) than to random (0.0385), that is, above the midpoint (0.0520). Since all the fragments are in English, the ones below the midpoint are English texts that the IC would confuse with random letters.

| Length | Minimum IC | Mean IC | Maximum IC | Fragments above the midpoint |
|---|---|---|---|---|
| 10 | 0.0000 | 0.0549 | 0.1556 | 42.0 % |
| 15 | 0.0095 | 0.0589 | 0.1333 | 57.5 % |
| 25 | 0.0300 | 0.0589 | 0.1067 | 62.0 % |
| 50 | 0.0424 | 0.0631 | 0.0931 | 92.0 % |
| 100 | 0.0515 | 0.0645 | 0.0885 | 99.5 % |
| 200 | 0.0576 | 0.0648 | 0.0770 | 100.0 % |
| 400 | 0.0571 | 0.0649 | 0.0725 | 100.0 % |

**Conclusion.** I trust the measurement from 100 letters: at that length, 199 of the 200 English fragments (99.5 %) are above the midpoint, and from 200 letters all of them are. Below that, part of the English texts would look random, as happens with `CRYPTANALYSIS`: with 25 letters, 38 % of the fragments are closer to random than to English, and with 10 letters the IC goes from 0 to 0.16, so it says nothing.

The mean gets close to the English value quite early (0.059 with 15 letters), but what matters is the spread: with few letters, each specific text can fall very far from the mean. With 100 letters, the minimum (0.0515) is already right at the midpoint, and with 200 or more it is clearly above it.

---

## 4. B2: Cipher family classifier

A transposition only changes the position of the letters, so it keeps the English frequencies. A substitution changes each letter into another one, and the frequencies no longer look like English. I measure that similarity with the chi-squared from Practice 1, divided by the length of the text, so that texts of different lengths can be compared with a single threshold. If the normalised χ² is lower than the threshold, the text is a transposition; otherwise, a substitution.

**How I chose the threshold.** For each length (60, 120, 250 and 400) I generated 150 columnar transpositions and 150 monoalphabetic substitutions, with random keys and random fragments of the reference text. Then I tried every threshold from 0.00 to 5.00, in steps of 0.01, and kept the one with the fewest errors in total.

- Threshold with X padding: **2.97** ← this is the one used by `classify`, because `encrypt` pads with X by default.
- Threshold with random padding: **0.97**

| Length | Error with X padding | Error with random padding |
|---|---|---|
| 60 | 5.3 % | 1.0 % |
| 120 | 3.3 % | 0.0 % |
| 250 | 3.0 % | 0.0 % |
| 400 | 4.3 % | 0.0 % |

The random padding is chosen letter by letter, at random, but giving more probability to the most frequent letters in English (for example, E comes up much more often than Z), so that the padding does not change the frequencies of the text. In the code this is done with `random.choices`, using the frequencies in `ENGLISH_FREQUENCIES` as weights.

**1. At which lengths does it work, and at which does it fail?**
With random padding it works at every length: 1 % error with 60 letters and 0 % from 120. With X padding it fails at every length: 5.3 % with 60 letters and between 3 % and 4.3 % for the rest. It fails most with 60 letters, because with few letters the frequencies depend a lot on chance and a few X of padding weigh much more. But the error does not disappear with long texts either, because the threshold had to rise to 2.97 to accept the transpositions with many X, and with such a high threshold some substitutions (the ones that look like English by chance) fall below it and are classified as transpositions, whatever the length.

**2. Why does changing only the padding character change the error so much?**
X is one of the rarest letters in English (0.15 %), so almost none are expected in a normal text. The chi-squared compares how many times each letter appears with how many times it is expected, and when almost none are expected, a few X of padding make the value rise a lot. That is why some transpositions look like substitutions, and the threshold has to be raised so that they are not misclassified. But with a higher threshold, some substitutions that look a bit like English fall below it and are classified as transpositions. With random padding this does not happen: the added letters follow the English frequencies, the chi-squared does not rise, and the two families stay well separated.

**3. How much the padding contributes in a 66-letter text with 6 X.**
I compute only the part of the chi-squared that corresponds to the letter X, assuming the original text had none:

- **Expected X** in 66 letters of English: 0.150 % × 66 = 0.099, that is, almost none.
- **Observed X:** the 6 from the padding.
- **Contribution of X:** (6 − 0.099)² / 0.099 ≈ 351.7
- **Divided by the length** (as `chi_squared` does): 351.7 / 66 ≈ 5.33

The 6 X of padding alone already add up to **5.33**, almost twice my threshold (2.97). That text would be classified as a substitution because of the padding, even if all the other letters were perfect English. Without padding, X would contribute only 0.0015.

**4. Design rule.**
Padding must not change the letter frequencies of the text. If a cipher needs padding, it should use letters chosen according to how common they are in the language, and not always repeat the same rare letter (like X). Otherwise, the padding leaves a mark that an attacker can exploit; in this case, to find out which type of cipher was used.

---

## 5. B3: Why not use the GCD instead of `factor_tally`?

**The idea behind Kasiski.** In Vigenère, if the same fragment of the original text (for example `THE`) falls twice at the same position of the key, it is encrypted the same way and appears repeated in the ciphertext. The distance between the two repetitions is then a multiple of the key length. That is why the key length is a number that divides the distances.

**Why the GCD seems to work.** The greatest common divisor (GCD) is the largest number that divides all the numbers in a list. With the test text, the distances are 15, 35 and 50, and their GCD is 5, which is the correct key length.

**The problem: chance repetitions.** Not all repetitions come from the key. Sometimes two different fragments of the original text, encrypted with different letters of the key, produce the same 3 letters by chance. The distance between them does not have to be a multiple of the key length.

For example, if a chance repetition at distance 21 is added to 15, 35 and 50:

- **GCD:** 21 is not a multiple of 5, so the only number that divides all four distances is 1. GCD(15, 35, 50, 21) = 1, which is wrong. And the function gives no warning: it returns 1 as if it were a valid answer.
- **`factor_tally`:** it counts how many distances each number divides, like a vote.

| Factor | 15 | 35 | 50 | 21 | Votes |
|---|---|---|---|---|---|
| 3 | yes | no | no | yes | 2 |
| **5** | yes | yes | yes | no | **3** |
| 7 | no | yes | no | yes | 2 |

5 loses one vote because of 21, but it still wins with 3 out of 4. A bad distance only takes away one vote; it does not ruin the whole result.

**Condition under which the GCD fails silently:** it is enough for a single distance not to be a multiple of the key length, that is, for there to be one chance repetition. The GCD needs all the distances to agree; the tally only needs the majority to agree. Since real texts almost always contain some chance repetition, especially with 3-letter fragments, `factor_tally` is much more reliable.

---

## 6. C1: Key length

**The idea.** A Vigenère with an `m`-letter key is, in fact, `m` Caesar ciphers mixed together. For example, with the key `CIPHER` (6 letters), the letters at positions 0, 6, 12, 18… are all encrypted with `C`, those at positions 1, 7, 13… with `I`, and so on. If the letters are grouped this way (each group is a coset), each group is a Caesar cipher. Since a Caesar cipher does not change the letter frequencies, only the names of the letters, the IC of each group looks like that of English (≈ 0.066).

If a wrong length is tried, each group mixes letters encrypted with several different letters of the key, the frequencies flatten out and the IC drops towards that of random letters (≈ 0.038). `coset_ic` splits the text into `m` groups and returns the average of their ICs: if it is high, `m` is probably the key length.

**What "clearly above" means in my code.** I set a threshold between the IC of random letters (1/26 ≈ 0.0385) and the IC of English (≈ 0.0655, obtained by adding up the square of each frequency in the table). The threshold is a fraction of the way between the two:

threshold = IC_random + fraction × (IC_language − IC_random)

That is, it starts from random and moves part of the way towards English. I chose the fraction with: `calibrar_fraccion` encrypts 200 texts of 400 letters with random keys of 3 to 10 letters, whose length I know, and counts which fraction gets it right most often:

| Fraction | Correct (out of 200) |
|---|---|
| 0.5 | 169 |
| 0.6 | 193 |
| **0.7** | **196** |
| 0.8 | 185 |
| 0.9 | 134 |

I chose 0.7, which in English gives a threshold of ≈ 0.0574. With a lower fraction, the threshold is so low that some wrong lengths exceed it (see below). With a higher one, sometimes not even the correct length reaches it, especially with short texts, where the IC is more irregular.

**Why the smallest `m` and not the highest.** `find_key_length` returns the smallest `m` whose average exceeds the threshold. The highest one cannot be chosen because multiples of the true length also give "pure" groups: with the 6-letter key and m = 12, the group at positions 0, 12, 24… also contains only letters encrypted with `C`. In the table below, m = 12 gives even more than m = 6.

**`coset_ic` table** (Vigenère with the key `CIPHER`, 6 letters, on 600 letters):

| m | coset_ic | | m | coset_ic | |
|---|---|---|---|---|---|
| 1 | 0.0434 | divisor | 9 | 0.0533 | |
| 2 | 0.0462 | divisor | 10 | 0.0457 | |
| 3 | 0.0522 | divisor | 11 | 0.0443 | |
| 4 | 0.0473 | | **12** | **0.0661** | **multiple** |
| 5 | 0.0433 | | 13 | 0.0428 | |
| **6** | **0.0649** | **true length** | 14 | 0.0466 | |
| 7 | 0.0442 | | 15 | 0.0514 | |
| 8 | 0.0482 | | 16 | 0.0493 | |

**What the table shows.** The IC of each `m` depends on how many different letters of the key each group mixes:

| m | Key letters in each group | coset_ic |
|---|---|---|
| 6, 12 | 1 (pure group) | 0.065 – 0.066 |
| 3, 9, 15 | 2 | 0.051 – 0.053 |
| 2, 4, 8, 10, 14, 16 | 3 | 0.046 – 0.049 |
| 1, 5, 7, 11, 13 | 6 (all) | 0.043 – 0.044 |

(In general, each group mixes 6 / gcd(m, 6) different letters of the key.)

For example, with m = 3 the first group has positions 0, 3, 6, 9…, which are encrypted with `C`, `H`, `C`, `H`…: only 2 letters of the key. It is a "half pure" group, so its IC falls halfway between random and English. That is why the threshold cannot be halfway (≈ 0.052): 3 would exceed it, and since the program returns the first one that passes, it would answer 3 instead of 6. With the fraction 0.7, only the pure groups exceed the threshold: the true length (6) and its multiple (12), and the program returns the smallest, 6.

---

## 7. C2: Automatic Vigenère attack

**How `attack` works.** It puts together everything above, without knowing anything about the key:

1. `find_key_length` (C1) computes the key length, for example 5.
2. `cosets` (Practice 1) splits the text into 5 groups. Each group is encrypted with a single letter of the key, so it is a Caesar cipher.
3. `break_caesar` (Practice 1) breaks each group: it tries the 26 shifts and keeps the one that gives the text most similar to English, according to the chi-squared.
4. Each shift is turned into a letter (for example, 11 → `L`) and putting them together gives the key.
5. `decrypt` (Practice 1) decrypts the text with that key.

**The tables.** Each cell is the success percentage over 100 trials, with random keys and random fragments of text. The first table measures whether the attack recovers the whole key, and the second whether it finds only the key length (step 1). Comparing them shows at which step the attack fails.

**Complete key recovered**

| Key \ Text | 100 | 150 | 200 | 300 | 400 |
|---|---|---|---|---|---|
| 3 | 72 % | 92 % | 91 % | 97 % | 100 % |
| 5 | 37 % | 86 % | 96 % | 98 % | 99 % |
| 7 | 18 % | 51 % | 70 % | 97 % | 98 % |
| 9 | 3 % | 29 % | 50 % | 84 % | 91 % |

**Correct key length**

| Key \ Text | 100 | 150 | 200 | 300 | 400 |
|---|---|---|---|---|---|
| 3 | 77 % | 92 % | 91 % | 97 % | 100 % |
| 5 | 75 % | 91 % | 96 % | 98 % | 99 % |
| 7 | 67 % | 82 % | 88 % | 97 % | 100 % |
| 9 | 59 % | 83 % | 86 % | 98 % | 97 % |

**1. Which quantity governs each table?**

- **Key length:** it depends mainly on the total length of the text (N). `coset_ic` averages all the groups, so it uses all the letters at once. That is why, for the same text length, it succeeds similarly for any key: with 200 letters, between 86 % and 96 %.
- **Complete key:** it depends on the number of letters in each group (N / m). Each Caesar cipher is broken only with the letters in its group, and all of them have to come out right: if a single letter of the key is wrong, the whole key is wrong. That is why this table drops much faster when the key is long.

**2. Why do 200 letters work with a 5-letter key and not with a 9-letter one?**

Because the text is split among the groups. With a 5-letter key, each group has 200 / 5 = 40 letters; with a 9-letter one, only 200 / 9 ≈ **22**. With 22 letters, the frequencies depend a lot on chance, and the chi-squared sometimes chooses the wrong shift. Also, 9 groups have to be right instead of 5, and the more groups there are, the more chances of failing in one of them. The key length is found well in both cases (96 % and 86 %); what fails is breaking the Caesar ciphers: the complete key drops from 96 % to 50 %.

**3. How much text is needed?**

 **N ≥ 40 × m**: the text must have at least 40 letters for each letter of the key.

The rule comes from my tables. The cells with about 40 letters per group recover the complete key in 91 % of cases or more:

| Key | Text | Letters per group | Complete key |
|---|---|---|---|
| 5 | 200 | 40 | 96 % |
| 7 | 300 | 43 | 97 % |
| 9 | 400 | 44 | 91 % |

If the key length is unknown, the calculation has to be done with the longest possible key. For example, if the key could be up to 10 letters long, at least 400 letters of text are needed.

---

## 8. C3: Breaking the columnar transposition

**How it works.** The number of columns (`n`) is known, but not the order in which they were read. With `n` columns there are `n!` possible orders (for example, with 4 columns there are 4 × 3 × 2 × 1 = 24). `attack` tries all of them with `itertools.permutations`: it decrypts the text with each order, gives it a score and keeps the one with the highest score.

**The bigram score.** A bigram is a pair of consecutive letters: in `THE` there are two, `TH` and `HE`. In English, some pairs are very common (`TH`, `HE`, `IN`) and others hardly appear (`QX`, `ZJ`). The score of a candidate text is the sum of `log p(xy)` for each pair of consecutive letters, so a text with many typical English pairs scores higher than one with rare pairs.

**The bigram table.** I built it by counting the pairs of consecutive letters in the first half of the reference text (*Pride and Prejudice*, about 9,400 letters). The test fragments come from the second half, so that the attack is not tested with sentences it has already seen. Each pair starts counting at 1, so that the ones that never appear in the book (like `QZ`) do not have probability 0, because `log(0)` would give an error.

**Why are letter frequencies useless?** Because all the candidate orders have exactly the same letters, only in different positions, so the chi-squared would give them all the same score; the only thing that changes between them is which letter is next to which, and that is what bigrams measure.

**Text recovered exactly** (100 trials per cell, with random keys and fragments):

| Columns | 60 letters | 120 letters | 200 letters |
|---|---|---|---|
| 4 | 100 % | 100 % | 100 % |
| 5 | 100 % | 100 % | 100 % |
| 6 | 99 % | 100 % | 100 % |
| 7 | 99 % | 100 % | 100 % |

The attack almost never fails because it tries every order, so the correct one is always among the candidates. It only failed twice, with 60-letter texts, where by chance a wrong order scored slightly higher.

**What is the largest `n` solved in under 10 seconds?**

| Columns | Orders (n!) | Time |
|---|---|---|
| 7 | 5,040 | 0.2 s |
| 8 | 40,320 | 1.8 s |
| 9 | 362,880 | 17.1 s |

**n = 8.** Each extra column multiplies the number of orders: going from 8 to 9 columns multiplies the orders by 9, and the time rises from 1.8 s to 17.1 s.

**How to go further (without implementing it).** Instead of trying every order, a local search (hill climbing) can be used:

1. Start with a random order.
2. Swap two columns.
3. If the bigram score improves, keep the change; if not, undo it.
4. Repeat until no swap improves the score.

Since it can sometimes get stuck in an order that is quite good but not correct, it is repeated several times starting from different random orders, and the best result is chosen. This way only a few thousand orders are tried, guided by the score, instead of all of them, and 15 or 20 columns can be attacked, where trying every order would be impossible.

---

## 9. Part D: the pipeline decides with a single number

Before trying any attack, `attack.py` decides whether the text is a transposition or a substitution by looking at a single number: the normalised chi-squared, which measures how similar the letter frequencies of the text are to those of the language (the IC is only used afterwards, to tell the two types of substitution apart). That number depends on a single property of the cipher: whether it keeps the letter frequencies or not. A transposition keeps them, because it only changes the position of the letters, and a substitution normally does not, because it changes some letters into others. That is why a cipher that changes the letters but keeps their frequencies would fool the classifier completely. For example, a substitution that only swaps letters that appear almost equally often in English (N with S, H with R, I with O,…) changes the whole text, but the frequencies hardly move, so its chi-squared would be almost the same as that of an English text. The pipeline would take it for a transposition and launch the wrong attack, which would never find the original text.

---

## 10. What does not work or has limits

- **Classifier with X padding:** it is wrong in 3–5 % of cases at every length (5.3 % with 60 letters). With random padding it would be almost perfect, but `encrypt` pads with X by default, as the handout requires, so `classify` uses the X-padding threshold.
- **Vigenère with short texts or long keys:** the complete key is poorly recovered below about 40 letters per group (see C2). Also, if a key repeats itself internally (for example, `ABCABC`), the short version (`ABC`) is found: the text is decrypted correctly, but the returned key is not the original one.
- **Transposition with many columns:** the attack tries every possible order, so from 9 columns it takes more than 10 seconds. Also, if `--cols` is not given, `attack.py` only tries 2 to 8 columns. If the text was encrypted with 9 columns or more, it returns the best result between 2 and 8, which will be meaningless text, without warning that it has failed.
- **Spanish:** the threshold of `classify` and the fraction of `find_key_length` were computed with English texts. With `--lang es` the Spanish frequency table is used, but those two values have not been tested with Spanish texts, so they may work worse. The bigram table of the columnar attack is also built only from the English reference text, so `break_columnar.attack` ignores `language` and always scores in English.
- **Working directory:** `break_columnar.py` opens `referencia.txt` with a relative path when it is imported, so it (and `attack.py`, which imports it) must be run from the main project folder.

---

## LLM assistance declaration

I used Claude (claude.ai) as an assistant throughout Parts A–D, in a single conversation. I always asked it to explain the reasoning behind a piece of code before accepting it, so that I could reproduce and justify every line myself. All the measurements in this report were run by me, and every number in the tables comes from my own executions.

- **`railfence.py` (A1).** I wrote the zigzag logic myself (the matrix with `direccion` and `rail_actual`), but my version computed the number of columns wrongly and crashed with an `IndexError`, and my `decrypt` repeated the same steps as `encrypt` instead of undoing them. Claude explained that each column holds `rails - 1` letters, fixed the column count, and rewrote `decrypt` reusing my own zigzag walk (mark the cells, fill them row by row, read them back in zigzag order).
- **`columnar.py` (A2, A3).** I wrote `key_order` and the first versions of `encrypt` and `decrypt`, but my first `encrypt` was wrong: it assumed the matrix had to be square (its size came from the square root of the text length) instead of having one column per letter of the keyword, so it skipped letters and did not match `decrypt`. Claude explained the correct structure (columns = keyword length, rows = as many as needed). For the double transposition, my first version simply called `encrypt` twice; I found out that it returned garbage when the length was not a multiple of both keys, Claude explained why, and proposed padding once to a multiple of `math.lcm` of both key lengths.
- **`measure.py` (B1, B2).** Claude designed the B2 measurement with me: `hacer_muestras` (generating transposition and substitution samples, including the random padding drawn from the English frequencies), `contar_errores` and `elegir_umbral` (choosing the threshold from data). It also helped me write the B1 experiment that runs in the `if __name__ == "__main__":` block (`experimento_ic`), which measures from which length the IC can be trusted.
- **`keylength.py` (C1).** Claude designed `calibrar_fraccion`, the experiment that chooses the threshold fraction from data instead of hard-coding it.
- **`break_columnar.py` (C3).** Claude wrote the exhaustive attack with bigram scoring and the measurement.
- **`attack.py` and `crypto.py` (Part D).** Claude extended my Practice 1 `crypto.py` with the `railfence`, `columnar` and `measure` subcommands, keeping all my existing commands.
- **`tests/`.** Claude wrote the test files. I ran them, and they helped me find several bugs in my own code (in `railfence.py` and `columnar.py`) that I then fixed.
- **This README.** I asked Claude to rephrase my own draft sentences into more precise, academic, and formal wording (correct terminology, more formal register) without changing what I was actually saying.