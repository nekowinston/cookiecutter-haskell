# SPDX-FileCopyrightText: 2025 winston <hey@winston.sh>
# SPDX-License-Identifier: MIT

import sys
from subprocess import run
from typing import Callable as C

info: C[[str], None] = lambda str: print(f"λ \033[1;36m{str}\033[1;0m")
warn: C[[str], None] = lambda str: print(f"λ \033[1;33m{str}\033[1;0m")
error: C[[str], None] = lambda str: print(f"λ \033[1;31m{str}\033[1;0m")

if __name__ == "__main__":
    try:
        _ = run(["nix", "--version"], capture_output=True, check=True)
    except Exception:
        error("Nix is not installed. You can't use this cookiecutter without it.")
        sys.exit(1)
