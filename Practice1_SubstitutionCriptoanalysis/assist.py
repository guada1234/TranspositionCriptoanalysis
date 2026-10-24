from basics import to_numbers, to_letters
from break_caesar import ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def eliminate_blanks(text: str) -> str:
    numbers = to_numbers(text)
    return to_letters(numbers)



def count_letters(text: str) -> dict[str, int]:
    dict = {}
    for letter in ALPHABET:
        dict[letter] = 0
    for char in text:
        dict[char] = dict[char] + 1
    return dict


def find_ngrams(text: str, n: int) -> dict[str, list[int]]: #desplizamos una ventana de tamaño n sobre el texto y guardamos las posiciones de cada ngrama en un diccionario
    positions = {}
    last_start = len(text) - n #donde empieza la ultima ventana de tamaño n
    for i in range(last_start + 1):
        semi_text = text[i:i + n]
        if semi_text not in positions:
            positions[semi_text] = []
        positions[semi_text].append(i)
    return positions



def report(ciphertext: str, language: str = "en") -> str:
    if language == "en":
        table = ENGLISH_FREQUENCIES
    elif language == "es":
        table = SPANISH_FREQUENCIES
    else:
        raise ValueError(f"unknown language '{language}', use 'en' for English or 'es' for Spanish")
 
    text = eliminate_blanks(ciphertext)
    total = len(text)
 
    lines = [] 
    lines.append(f"Frequency assistant report ({total} letters, language={language})")

    lines.append("")
    lines.append("Letter frequencies (ciphertext) vs expected distribution:")
    counts = count_letters(text)
 
    pairs = []
    for letter in ALPHABET:
        pairs.append((counts[letter], letter))

    pairs.sort(reverse=True) #ordenamos de mayor a menor por la cantidad de veces que aparece cada letra en el texto cifrado

    cipher_ranking = []
    for element in pairs:
        count = element[0]
        letter = element[1]
        cipher_ranking.append(letter) #ya queda ordenado de mayor a menor por la cantidad de veces que aparece cada letra en el texto cifrado

    for letter in cipher_ranking:
        count = counts[letter]
        if total > 0:
            percentage = (count / total) * 100
        else:
            percentage = 0.0
        
        expected = table[letter]
        lines.append(
            f"  {letter}: {count:3d} times  ({percentage:5.2f}%)   "
            f"expected for a plaintext letter: {expected:5.2f}%"
        )
 

    
    lines.append("")
    lines.append("Repeated trigrams (3-letter chunks appearing more than once):")
    trigrams = find_ngrams(text, 3)
    repeated_trigrams = []
    for semi_text in trigrams:
        if len(trigrams[semi_text]) >= 2:
            repeated_trigrams.append(semi_text)
    
    pairs = []
    for semi_text in repeated_trigrams:
        pairs.append((len(trigrams[semi_text]), semi_text)) #creamos una lista de tuplas (cantidad de veces que aparece el trigram, trigram) para poder ordenarlas por cantidad de veces que aparece cada trigram

    pairs.sort(reverse=True)

    repeated_trigrams = []
    for count, semi_text in pairs:
        repeated_trigrams.append(semi_text) #ya queda ordenado de mayor a menor por la cantidad de veces que aparece cada trigram
 
    if len(repeated_trigrams) == 0:
        lines.append("  (none found)")
    
    for semi_text in repeated_trigrams:
        positions = trigrams[semi_text]
        lines.append(f"  {semi_text}: {len(positions)} times, at positions {positions}")
 

    
    lines.append("")
    lines.append("Ten most frequent bigrams (2-letter chunks):")
    bigrams = find_ngrams(text, 2)
    pairs = []
    for semi_text in bigrams:
        pairs.append((len(bigrams[semi_text]), semi_text))

    pairs.sort(reverse=True)

    bigram_ranking = []
    for count, semi_text in pairs:
        bigram_ranking.append(semi_text)
 
    top_ten = bigram_ranking[:10]
    for semi_text in top_ten:
        positions = bigrams[semi_text]
        lines.append(f"  {semi_text}: {len(positions)} times")
 


    
    lines.append("")
    lines.append("Doubled letters (the same letter twice in a row):")
    doubled_found = False
    for i in range(len(text) - 1):
        if text[i] == text[i + 1]:
            doubled_found = True
            lines.append(f"  '{text[i]}{text[i]}' at position {i}")
    if not doubled_found:
        lines.append("  (none found)")
 


    
    lines.append("")
    lines.append("Suggested initial mapping (align the two rankings above):") #ordenar las letras del alfabeto por frecuencia de aparición en el texto cifrado y compararlas con la frecuencia esperada de aparición de las letras en el idioma elegido, para sugerir un mapeo inicial entre las letras del alfabeto cifrado y las letras del alfabeto plano
    pairs = []
    for letter in ALPHABET:
        pairs.append((table[letter], letter))

    pairs.sort(reverse=True)

    plain_ranking = []
    for element in pairs:
        frequency = element[0]
        letter = element[1]
        plain_ranking.append(letter)
 
    for i in range(26):
        cipher_letter = cipher_ranking[i]
        guess = plain_ranking[i]
        lines.append(f"  {cipher_letter} -> {guess}")
 
    return "\n".join(lines)

