# SPDX-FileCopyrightText: 2025 winston <hey@winston.sh>
# SPDX-License-Identifier: MIT

import pathlib
import shutil
import subprocess
from typing import Callable as C

info: C[[str], None] = lambda str: print(f"λ \033[1;33m{str}\033[1;0m")
warn: C[[str], None] = lambda str: print(f"λ \033[1;31m{str}\033[1;0m")
error: C[[str], None] = lambda str: print(f"λ \033[1;41m{str}\033[1;0m")
nix_run: C[[list[str]], int] = lambda args: subprocess.call(
    ["nix", "run", "--inputs-from", ".", f"nixpkgs#{args[0]}"] + (["--"] + args[1:])
)

if __name__ == "__main__":
    if "{{ cookiecutter.use_reuse }}" == "True":
        info("Setting up REUSE...")
        # only keep the used licenses
        for f in pathlib.Path("LICENSES").iterdir():
            if f.name not in ["CC0-1.0.txt", "{{ cookiecutter.license }}.txt"]:
                f.unlink()
    else:
        info("Setting up the LICENSE...")
        license = pathlib.Path("LICENSES/{{ cookiecutter.license }}.txt")
        _ = shutil.move(license, "LICENSE")

        shutil.rmtree(pathlib.Path("LICENSES"))
        pathlib.Path("REUSE.toml").unlink()

    info("Initializing flake.lock...")
    _ = subprocess.call(["nix", "flake", "lock"])

    info("Running the initial hpack...")
    _ = nix_run(["hpack"])

    info("Running fourmolu...")
    _ = nix_run(["fourmolu", "-i", "app", "src"])

    info("Running nix fmt")
    _ = subprocess.call(["nix", "fmt", "--", "flake.nix"])

    if "{{ cookiecutter.is_executable }}" == "False":
        shutil.rmtree(pathlib.Path("app"))

    if "{{ cookiecutter.is_library }}" == "False":
        shutil.rmtree(pathlib.Path("src"))

    info("Initializing Git...")
    _ = subprocess.call(["git", "init"], stdout=subprocess.DEVNULL)
    _ = subprocess.call(["git", "add", "--all"], stdout=subprocess.DEVNULL)
    _ = subprocess.call(
        ["git", "commit", "-m", "feat: initial commit"], stdout=subprocess.DEVNULL
    )

    info("Running initial pre-commit hooks...")
    _ = subprocess.call(["nix", "flake", "check"])

    info("Preparing devShell...")
    _ = subprocess.call(["nix", "develop", "-c", "true"])
