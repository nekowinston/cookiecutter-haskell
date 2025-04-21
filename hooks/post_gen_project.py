# SPDX-FileCopyrightText: 2025 winston <hey@winston.sh>
# SPDX-License-Identifier: MIT

from pathlib import Path
from shutil import move, rmtree
from subprocess import call, DEVNULL
from typing import Callable as C

info: C[[str], None] = lambda str: print(f"λ \033[1;36m{str}\033[1;0m")
warn: C[[str], None] = lambda str: print(f"λ \033[1;33m{str}\033[1;0m")
error: C[[str], None] = lambda str: print(f"λ \033[1;31m{str}\033[1;0m")
nix_run: C[[list[str]], int] = lambda args: call(
    ["nix", "run", "--inputs-from", ".", f"nixpkgs#{args[0]}"] + (["--"] + args[1:])
)

if __name__ == "__main__":
    if "{{ cookiecutter.use_reuse }}" == "True":
        info("Setting up REUSE...")
        # only keep the used licenses
        for f in Path("LICENSES").iterdir():
            if f.name not in ["CC0-1.0.txt", "{{ cookiecutter.license }}.txt"]:
                f.unlink()
    else:
        info("Setting up the LICENSE...")
        license = Path("LICENSES/{{ cookiecutter.license }}.txt")
        _ = move(license, "LICENSE")

        rmtree(Path("LICENSES"))
        Path("REUSE.toml").unlink()

    info("Initializing flake.lock...")
    _ = call(["nix", "flake", "lock"])

    info("Running the initial hpack...")
    _ = nix_run(["hpack"])

    info("Running fourmolu...")
    _ = nix_run(["fourmolu", "-i", "app", "src"])

    info("Running nix fmt")
    _ = call(["nix", "fmt", "--", "flake.nix"])

    if "{{ cookiecutter.is_executable }}" == "False":
        rmtree(Path("app"))

    if "{{ cookiecutter.is_library }}" == "False":
        rmtree(Path("src"))

    info("Initializing Git...")
    _ = call(["git", "init"], stdout=DEVNULL)
    _ = call(["git", "add", "--all"], stdout=DEVNULL)
    _ = call(
        ["git", "commit", "-m", "feat: initial commit"], stdout=DEVNULL
    )

    info("Running initial pre-commit hooks...")
    _ = call(["nix", "flake", "check"])

    info("Preparing devShell...")
    _ = call(["nix", "develop", "-c", "true"])
