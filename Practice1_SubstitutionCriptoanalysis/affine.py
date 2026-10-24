from basics import to_numbers, to_letters, modinv, egcd


def check_valid_a(a: int) -> None:
    g, _, _ = egcd(a, 26)
    if g != 1:
        raise ValueError(f"a={a} is not a valid key: gcd(a, 26) = {g}, must be 1")

#encrypt: E(x) = (a * x + b) mod 26
def encrypt(plaintext: str, a: int, b: int) -> str:
    check_valid_a(a)
    numbers = to_numbers(plaintext)
    encrypted = []
    for n in numbers:
        encrypted.append(a * n + b) #solo calculamos el valor de la formula, el mod 26 lo hacemos en la funcion to_letters
    return to_letters(encrypted)

#decrypt: D(y) = a_inverse * (y - b) mod 26
def decrypt(ciphertext: str, a: int, b: int) -> str:
    check_valid_a(a)
    a_inv = modinv(a, 26) 
    numbers = to_numbers(ciphertext)
    decrypted = []
    for n in numbers:
        decrypted.append(a_inv * (n - b)) 
    return to_letters(decrypted)


def valid_keys() -> list[tuple[int, int]]: #calculamos todas las claves validas (a,b) para el cifrado affine, donde a es coprimo con 26 y b puede ser cualquier numero entre 0 y 25
    keys = []
    for a in range(1, 26):
        g, _, _ = egcd(a, 26)
        if g == 1:
            for b in range(26):
                keys.append((a, b))
    return keys
