"""
Password Generator
Generates secure random passwords with configurable options.
"""

import argparse
import secrets
import string
import sys


def generate_password(length: int, use_upper: bool, use_lower: bool,
                      use_digits: bool, use_symbols: bool, exclude: str) -> str:
    """Build the character pool and generate a secure password."""
    pool = ""
    required_chars = []

    if use_upper:
        chars = "".join(c for c in string.ascii_uppercase if c not in exclude)
        pool += chars
        if chars:
            required_chars.append(secrets.choice(chars))

    if use_lower:
        chars = "".join(c for c in string.ascii_lowercase if c not in exclude)
        pool += chars
        if chars:
            required_chars.append(secrets.choice(chars))

    if use_digits:
        chars = "".join(c for c in string.digits if c not in exclude)
        pool += chars
        if chars:
            required_chars.append(secrets.choice(chars))

    if use_symbols:
        chars = "".join(c for c in string.punctuation if c not in exclude)
        pool += chars
        if chars:
            required_chars.append(secrets.choice(chars))

    if not pool:
        print("Error: No character set selected. Enable at least one character type.")
        sys.exit(1)

    if length < len(required_chars):
        print(f"Error: Password length ({length}) is too short to include all required character types ({len(required_chars)}).")
        sys.exit(1)

    # Fill the remaining length with random chars from the full pool
    remaining = [secrets.choice(pool) for _ in range(length - len(required_chars))]
    password_chars = required_chars + remaining

    # Shuffle to avoid required chars always appearing at the start
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def main():
    parser = argparse.ArgumentParser(
        description="🔐 Secure Password Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python password.py
  python password.py --length 20
  python password.py --length 16 --no-symbols
  python password.py --length 12 --no-upper --no-symbols
  python password.py --count 5 --length 24
  python password.py --length 16 --exclude "O0lI1"
        """
    )

    parser.add_argument(
        "--length", "-l",
        type=int,
        default=16,
        help="Length of the password (default: 16)"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)"
    )
    parser.add_argument(
        "--no-upper",
        action="store_false",
        dest="use_upper",
        help="Exclude uppercase letters (A-Z)"
    )
    parser.add_argument(
        "--no-lower",
        action="store_false",
        dest="use_lower",
        help="Exclude lowercase letters (a-z)"
    )
    parser.add_argument(
        "--no-digits",
        action="store_false",
        dest="use_digits",
        help="Exclude digits (0-9)"
    )
    parser.add_argument(
        "--no-symbols",
        action="store_false",
        dest="use_symbols",
        help="Exclude symbols (!@#$...)"
    )
    parser.add_argument(
        "--exclude", "-e",
        type=str,
        default="",
        help='Characters to exclude (e.g. --exclude "O0lI1" to avoid lookalikes)'
    )

    parser.set_defaults(use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
    args = parser.parse_args()

    if args.length < 4:
        print("Error: Password length must be at least 4.")
        sys.exit(1)

    if args.count < 1:
        print("Error: Count must be at least 1.")
        sys.exit(1)

    print(f"\n🔐 Generated Password{'s' if args.count > 1 else ''}:\n")
    for i in range(args.count):
        pwd = generate_password(
            length=args.length,
            use_upper=args.use_upper,
            use_lower=args.use_lower,
            use_digits=args.use_digits,
            use_symbols=args.use_symbols,
            exclude=args.exclude
        )
        if args.count > 1:
            print(f"  [{i+1}] {pwd}")
        else:
            print(f"  {pwd}")

    print(f"\n  Length : {args.length}")
    print(f"  Upper  : {'✓' if args.use_upper else '✗'}")
    print(f"  Lower  : {'✓' if args.use_lower else '✗'}")
    print(f"  Digits : {'✓' if args.use_digits else '✗'}")
    print(f"  Symbols: {'✓' if args.use_symbols else '✗'}")
    if args.exclude:
        print(f"  Exclude: {args.exclude}")
    print()


if __name__ == "__main__":
    main()