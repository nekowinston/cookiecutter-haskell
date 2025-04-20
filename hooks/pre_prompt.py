import sys
import subprocess


def error(s: str):
    print(f"λ \033[1;41m{s}\033[1;0m")


def nix_is_installed() -> bool:
    try:
        _ = subprocess.run(["nix", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if not nix_is_installed():
        print("Nix is not installed. You can't use this cookiecutter without it.")
        sys.exit(1)
