#!/usr/bin/env python3
"""
Password Generator
-------------------
A simple, secure, and user-friendly command-line tool for generating
strong, randomized passwords with customizable length and character sets.

Uses Python's `secrets` module (cryptographically secure) instead of
`random`, so passwords are safe to actually use.

Usage examples:
    python password_generator.py
    python password_generator.py -l 20
    python password_generator.py -l 16 --no-symbols
    python password_generator.py -l 12 -n 5
"""

import argparse
import secrets
import string
import sys

AMBIGUOUS_CHARS = "Il1O0"


def build_character_pool(use_upper=True, use_lower=True, use_digits=True,
                          use_symbols=True, exclude_ambiguous=False):
    """Build the pool of characters to draw the password from."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    if exclude_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)

    if not pool:
        raise ValueError("At least one character type must be selected.")

    return pool


def generate_password(length=12, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True,
                       exclude_ambiguous=False):
    """
    Generate a single cryptographically secure random password.

    Guarantees at least one character from each selected character
    type (when length allows), so passwords aren't accidentally
    all-digits or all-letters.
    """
    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    pool = build_character_pool(use_upper, use_lower, use_digits,
                                 use_symbols, exclude_ambiguous)

    # Collect one guaranteed character from each active category.
    required_chars = []
    categories = []
    if use_upper:
        categories.append(string.ascii_uppercase)
    if use_lower:
        categories.append(string.ascii_lowercase)
    if use_digits:
        categories.append(string.digits)
    if use_symbols:
        categories.append("!@#$%^&*()-_=+[]{}|;:,.<>?/")

    if exclude_ambiguous:
        categories = ["".join(c for c in cat if c not in AMBIGUOUS_CHARS)
                      for cat in categories]

    for cat in categories:
        if cat:
            required_chars.append(secrets.choice(cat))

    remaining_length = length - len(required_chars)
    random_chars = [secrets.choice(pool) for _ in range(remaining_length)]

    password_chars = required_chars + random_chars

    # Shuffle securely so the guaranteed chars aren't always at the front.
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def estimate_strength(password):
    """Return a rough, human-readable strength label for a password."""
    length = len(password)
    variety = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password),
    ])

    if length >= 16 and variety >= 3:
        return "Very Strong"
    elif length >= 12 and variety >= 3:
        return "Strong"
    elif length >= 8 and variety >= 2:
        return "Moderate"
    else:
        return "Weak"


def run_cli():
    parser = argparse.ArgumentParser(
        description="Generate strong, secure, random passwords."
    )
    parser.add_argument("-l", "--length", type=int, default=12,
                         help="Password length (default: 12)")
    parser.add_argument("-n", "--number", type=int, default=1,
                         help="Number of passwords to generate (default: 1)")
    parser.add_argument("--no-upper", action="store_true",
                         help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true",
                         help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true",
                         help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                         help="Exclude symbols")
    parser.add_argument("--exclude-ambiguous", action="store_true",
                         help="Exclude ambiguous characters (I, l, 1, O, 0)")
    parser.add_argument("-i", "--interactive", action="store_true",
                         help="Run in interactive (menu-driven) mode")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        run_interactive()
        return

    try:
        for _ in range(args.number):
            pwd = generate_password(
                length=args.length,
                use_upper=not args.no_upper,
                use_lower=not args.no_lower,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous,
            )
            print(f"{pwd}   [{estimate_strength(pwd)}]")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def ask_yes_no(prompt, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "
    answer = input(prompt + suffix).strip().lower()
    if answer == "":
        return default
    return answer in ("y", "yes")


def run_interactive():
    print("=" * 45)
    print("      SECURE PASSWORD GENERATOR")
    print("=" * 45)

    try:
        length_input = input("Password length (default 12): ").strip()
        length = int(length_input) if length_input else 12

        use_upper = ask_yes_no("Include uppercase letters?", True)
        use_lower = ask_yes_no("Include lowercase letters?", True)
        use_digits = ask_yes_no("Include digits?", True)
        use_symbols = ask_yes_no("Include symbols?", True)
        exclude_ambiguous = ask_yes_no(
            "Exclude ambiguous characters (I, l, 1, O, 0)?", False)

        count_input = input("How many passwords to generate? (default 1): ").strip()
        count = int(count_input) if count_input else 1

        print("\nGenerated Password(s):")
        print("-" * 45)
        for _ in range(count):
            pwd = generate_password(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous,
            )
            print(f"  {pwd}   [{estimate_strength(pwd)}]")
        print("-" * 45)

    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)


if __name__ == "__main__":
    run_cli()
