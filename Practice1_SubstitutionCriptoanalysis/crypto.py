import argparse
import sys
import caesar
import affine
import monoalpha
import vigenere
from break_caesar import break_caesar
from break_affine import break_affine
from break_vigenere import break_vigenere
from assist import report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crypto.py")
    subparsers = parser.add_subparsers(dest="cipher", required=True)

    # --- caesar ----------------------------------------------------------
    caesar_parser = subparsers.add_parser("caesar")
    caesar_parser.add_argument("mode", choices=["encrypt", "decrypt"])
    caesar_parser.add_argument("--key", type=int, required=True)
    caesar_parser.add_argument("--in", dest="infile")
    caesar_parser.add_argument("--out", dest="outfile")

    # --- affine ------------------------------------------------------------
    affine_parser = subparsers.add_parser("affine")
    affine_parser.add_argument("mode", choices=["encrypt", "decrypt"])
    affine_parser.add_argument("--a", type=int, required=True)
    affine_parser.add_argument("--b", type=int, required=True)
    affine_parser.add_argument("--in", dest="infile")
    affine_parser.add_argument("--out", dest="outfile")

    # --- mono ----------------------------------------------------------------
    mono_parser = subparsers.add_parser("mono")
    mono_parser.add_argument("mode", choices=["encrypt", "decrypt"])
    mono_parser.add_argument("--keyword")     # build the key from a keyword...
    mono_parser.add_argument("--key")          # ...or give the full 26-letter key directly
    mono_parser.add_argument("--in", dest="infile")
    mono_parser.add_argument("--out", dest="outfile")

    # --- vigenere -------------------------------------------------------------
    vigenere_parser = subparsers.add_parser("vigenere")
    vigenere_parser.add_argument("mode", choices=["encrypt", "decrypt"])
    vigenere_parser.add_argument("--key", required=True)
    vigenere_parser.add_argument("--in", dest="infile")
    vigenere_parser.add_argument("--out", dest="outfile")

    # --- break -------------------------------------------------------------
    break_parser = subparsers.add_parser("break")
    break_parser.add_argument("target", choices=["caesar", "affine", "vigenere"])
    break_parser.add_argument("--m", type=int)              # only needed for vigenere
    break_parser.add_argument("--lang", default="en", choices=["en", "es"])
    break_parser.add_argument("--in", dest="infile")
    break_parser.add_argument("--out", dest="outfile")

    # --- assist -----------------------------------------------------------
    assist_parser = subparsers.add_parser("assist")
    assist_parser.add_argument("--lang", default="en", choices=["en", "es"])
    assist_parser.add_argument("--in", dest="infile")
    assist_parser.add_argument("--out", dest="outfile")

    return parser


def read_input(args: argparse.Namespace) -> str:
    """Read from --in FILE if given, otherwise from standard input."""
    if args.infile is not None:
        with open(args.infile, "r") as f:
            return f.read()
    return sys.stdin.read()


def write_output(args: argparse.Namespace, text: str) -> None:
    """Write to --out FILE if given, otherwise to standard output."""
    if args.outfile is not None:
        with open(args.outfile, "w") as f:
            f.write(text)
    else:
        print(text)


def run(args: argparse.Namespace) -> str:
    """
    Do the actual work for whichever subcommand was chosen, and
    return the text that should be written out.
    """
    if args.cipher == "caesar":
        text = read_input(args)
        if args.mode == "encrypt":
            return caesar.encrypt(text, args.key)
        else:
            return caesar.decrypt(text, args.key)

    if args.cipher == "affine":
        text = read_input(args)
        if args.mode == "encrypt":
            return affine.encrypt(text, args.a, args.b)
        else:
            return affine.decrypt(text, args.a, args.b)

    if args.cipher == "mono":
        text = read_input(args)
        if args.keyword is not None:
            key = monoalpha.key_from_keyword(args.keyword)
        elif args.key is not None:
            key = args.key
        else:
            raise ValueError("mono needs either --keyword or --key")
        if args.mode == "encrypt":
            return monoalpha.encrypt(text, key)
        else:
            return monoalpha.decrypt(text, key)

    if args.cipher == "vigenere":
        text = read_input(args)
        if args.mode == "encrypt":
            return vigenere.encrypt(text, args.key)
        else:
            return vigenere.decrypt(text, args.key)

    if args.cipher == "break":
        text = read_input(args)
        if args.target == "caesar":
            key, plaintext = break_caesar(text, args.lang)
            return f"key found: {key}\n{plaintext}"
        if args.target == "affine":
            key, plaintext = break_affine(text, args.lang)
            return f"key found: a={key[0]}, b={key[1]}\n{plaintext}"
        if args.target == "vigenere":
            if args.m is None:
                raise ValueError("break vigenere needs --m (the key length)")
            key, plaintext = break_vigenere(text, args.m, args.lang)
            return f"key found: {key}\n{plaintext}"

    if args.cipher == "assist":
        text = read_input(args)
        return report(text, args.lang)

    raise ValueError(f"unknown cipher '{args.cipher}'")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run(args)
        write_output(args, result)
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()