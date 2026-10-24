import basics
 
REFERENCE_TEXT_EN = basics.to_letters(basics.to_numbers("""
Cryptography is the practice of protecting information by transforming
it so that only the people who are supposed to read it can understand
it. For centuries, before computers existed, people used pen and paper
ciphers to hide military and diplomatic messages from their enemies.
A substitution cipher simply replaces each letter of the alphabet with
a different letter, following some fixed rule that both the sender and
the receiver agree on in advance. The weakness of these old ciphers is
that ordinary language has a very predictable letter distribution, so
an attacker who has enough ciphertext can often recover the key using
nothing more than counting and a bit of patience, without ever needing
to guess the key directly by brute force.
"""))
 
REFERENCE_TEXT_ES = basics.to_letters(basics.to_numbers("""
La criptografia es la practica de proteger informacion transformandola
para que solo las personas autorizadas puedan entenderla. Durante
siglos, mucho antes de que existieran los ordenadores, se usaban
cifrados de papel y lapiz para esconder mensajes militares y
diplomaticos de los enemigos. Un cifrado por sustitucion simplemente
cambia cada letra del alfabeto por otra letra distinta, siguiendo una
regla fija que tanto el emisor como el receptor conocen de antemano.
La debilidad de estos cifrados antiguos es que el lenguaje normal
tiene una distribucion de letras muy predecible.
"""))