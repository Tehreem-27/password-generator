# 🔐 Password Generator

A simple, secure Python tool for generating strong, randomized passwords with fully customizable length and character options.

Built with Python's `secrets` module — the cryptographically secure random generator recommended for passwords, tokens, and other security-sensitive values (unlike the standard `random` module).

## Features

- ✅ Cryptographically secure randomness (`secrets`, not `random`)
- ✅ Customizable password length
- ✅ Toggle uppercase, lowercase, digits, and symbols on/off
- ✅ Option to exclude ambiguous characters (`I`, `l`, `1`, `O`, `0`)
- ✅ Generate multiple passwords at once
- ✅ Built-in password strength indicator
- ✅ Two modes: quick command-line flags **or** a friendly interactive menu
- ✅ Zero dependencies — pure Python standard library

## Requirements

- Python 3.7+
- No external packages needed

## Installation

```bash
git clone https://github.com/<your-username>/password-generator.git
cd password-generator
```

## Usage

### Interactive mode (beginner-friendly)

Just run the script with no arguments and answer the prompts:

```bash
python password_generator.py
```

```
=============================================
      SECURE PASSWORD GENERATOR
=============================================
Password length (default 12): 16
Include uppercase letters? [Y/n]:
Include lowercase letters? [Y/n]:
Include digits? [Y/n]:
Include symbols? [Y/n]:
Exclude ambiguous characters (I, l, 1, O, 0)? [y/N]:
How many passwords to generate? (default 1): 3

Generated Password(s):
---------------------------------------------
  Vj%{}ng<ckTsW|0I   [Very Strong]
  UP1n&0m]KQDlT%M2   [Very Strong]
  +1rj%zBPb|ndv+zj   [Very Strong]
---------------------------------------------
```

### Command-line mode (fast, scriptable)

```bash
# Default: one 12-character password
python password_generator.py

# Custom length
python password_generator.py -l 20

# Generate 5 passwords at once
python password_generator.py -l 16 -n 5

# Exclude symbols
python password_generator.py -l 14 --no-symbols

# Exclude ambiguous characters (great for passwords typed by hand)
python password_generator.py -l 16 --exclude-ambiguous
```

### All options

| Flag | Description |
|------|-------------|
| `-l`, `--length` | Password length (default: 12) |
| `-n`, `--number` | Number of passwords to generate (default: 1) |
| `--no-upper` | Exclude uppercase letters |
| `--no-lower` | Exclude lowercase letters |
| `--no-digits` | Exclude digits |
| `--no-symbols` | Exclude symbols |
| `--exclude-ambiguous` | Exclude ambiguous characters (`I`, `l`, `1`, `O`, `0`) |
| `-i`, `--interactive` | Force interactive menu mode |

### Use it as a module

```python
from password_generator import generate_password

pwd = generate_password(length=16, use_symbols=False)
print(pwd)
```

## How it works

1. Builds a character pool from the selected categories (uppercase, lowercase, digits, symbols).
2. Guarantees at least one character from each selected category, so you never end up with an "all-digit" password by chance.
3. Fills the rest of the password with securely random characters from the pool.
4. Shuffles the result using `secrets.randbelow` so the guaranteed characters aren't predictably placed.

## License

Released under the [MIT License](LICENSE).
