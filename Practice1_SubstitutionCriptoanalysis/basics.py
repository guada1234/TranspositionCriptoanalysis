


def to_numbers(text: str) -> list[int]:
    new_text = text.upper()
    numbers = []
    for char in new_text:
        if 'A' <= char <= 'Z':
            normalized_letter = ord(char) - ord('A') #de letra a numero
            numbers.append(normalized_letter)

    return numbers

def to_letters(nums: list[int]) -> str:
    text = ""
    for num in nums:
        normalized_number = (num % 26) + ord('A')
        text += chr(normalized_number) #de numero a letra

    return text

def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0

    remainder = a % b
    gcd, x, y = egcd(b, remainder) #gcd = max comun divisor
    new_x = y
    new_y = x - (a // b) * y
    return gcd, new_x, new_y

#hallar x/ a⋅x≡1(modm)
def modinv(a: int, m: int) -> int:
    gcd, x, y = egcd(a, m)

    if gcd != 1: #para que exista un inverso  necesitamos: gcd(a,m)=1
        raise ValueError(f"No modular inverse for {a} modulo {m}")

    result = x % m #para que quede en el rango, en caso de que x sea negativo se hace el mod
    return result


def xor_bytes(data: bytes, key: bytes) -> bytes:
    result = b""

    for i in range(len(data)):
        data_byte = data[i]
        key_byte = key[i % len(key)] #vuelve a empezar desde el principio de la clave si es mas corta que el texto
        xor = data_byte ^ key_byte 
        result += bytes([xor])
    return result
