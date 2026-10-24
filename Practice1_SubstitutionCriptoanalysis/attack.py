import argparse
from Practice1_SubstitutionCriptoanalysis.basics import to_numbers, to_letters
from Practice1_SubstitutionCriptoanalysis.break_caesar import ENGLISH_FREQUENCIES, SPANISH_FREQUENCIES, chi_squared
from Practice1_SubstitutionCriptoanalysis.assist import report
from measure import index_of_coincidence, classify, UMBRAL
import keylength
import break_vigenere
import break_columnar


def ic_del_idioma(tabla):
    ic = 0.0
    for letra in tabla:
        p = tabla[letra] / 100
        ic += p * p
    return ic


def atacar_sustitucion(texto, lang, tabla):
    ic = index_of_coincidence(texto)
    ic_azar = 1 / 26
    ic_idioma = ic_del_idioma(tabla)
    limite = (ic_azar + ic_idioma) / 2
    print(f"IC del texto: {ic:.4f}  (azar {ic_azar:.4f}, idioma {ic_idioma:.4f}, límite {limite:.4f})")

    if ic > limite:
        print("Decisión: IC alto -> monoalfabética")
        print()
        print(report(texto, lang))
        return

    print("Decisión: IC bajo -> polialfabética (Vigenère)")
    print()
    m = keylength.find_key_length(texto, language=lang)
    umbral = 1 / 26 + keylength.FRACCION * (ic_idioma - 1 / 26)
    print(f"coset_ic por m (umbral {umbral:.4f}):")
    for i in range(1, 17):
        marca = "  <- largo elegido" if i == m else ""
        print(f"  m = {i:2}: {keylength.coset_ic(texto, i):.4f}{marca}")

    clave, plano = break_vigenere.attack(texto, lang)
    print()
    print("Clave:", clave)
    print("Texto:", plano)


def puntuar(texto):
    score = 0
    for i in range(len(texto) - 1):
        score += break_columnar.bigramas[texto[i:i + 2]]
    return score


def atacar_transposicion(texto, lang, cols):
    if cols is not None:
        candidatos = [cols]
    else:
        candidatos = []
        for n in range(2, 9):
            if len(texto) % n == 0:
                candidatos.append(n)
        print("Probando columnas que dividen", len(texto), ":", candidatos)

    if len(candidatos) == 0:
        print("Ningún número de columnas entre 2 y 8 divide el largo del texto.")
        return

    mejor = None
    for n in candidatos:
        orden, plano = break_columnar.attack(texto, n, lang)
        score = puntuar(plano)
        print(f"  {n} columnas: orden {orden}, puntuación de bigramas {score:.1f}")
        if mejor is None or score > mejor[0]:
            mejor = (score, n, orden, plano)

    score, n, orden, plano = mejor
    print()
    print("Columnas:", n)
    print("Orden:", orden)
    print("Texto:", plano)


def main():
    parser = argparse.ArgumentParser(description="Ataque automático")
    parser.add_argument("--in", dest="archivo", required=True)
    parser.add_argument("--lang", choices=["en", "es"], default="en")
    parser.add_argument("--cols", type=int)
    args = parser.parse_args()

    with open(args.archivo, encoding="utf-8") as f:
        texto = to_letters(to_numbers(f.read()))

    if args.lang == "es":
        tabla = SPANISH_FREQUENCIES
    else:
        tabla = ENGLISH_FREQUENCIES

    # 1. Medidas y clasificación
    print("Largo:", len(texto), "letras")
    print(f"Índice de coincidencia: {index_of_coincidence(texto):.4f}")
    print(f"Chi-cuadrado normalizado: {chi_squared(texto, tabla):.4f}  (umbral {UMBRAL})")
    familia = classify(texto, args.lang)
    print("Familia:", familia)
    print()

    # 2. Ataque según la familia
    if familia == "transposition":
        atacar_transposicion(texto, args.lang, args.cols)
    else:
        atacar_sustitucion(texto, args.lang, tabla)


if __name__ == "__main__":
    main()