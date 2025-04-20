#!/usr/bin/env python
import pathlib
import shutil
import subprocess


def info(s: str):
    print(f"λ \033[1;33m{s}\033[1;0m")


def warn(s: str):
    print(f"λ \033[1;31m{s}\033[1;0m")


def error(s: str):
    print(f"λ \033[1;41m{s}\033[1;0m")


def nix_run(args: list[str]) -> int:
    cmd, *args = args
    if len(args) > 0:
        args.insert(0, "--")

    return subprocess.call(
        ["nix", "run", "--inputs-from", ".", f"nixpkgs#{cmd}"] + args
    )


if __name__ == "__main__":
    info("Initializing flake.lock...")
    _ = subprocess.call(["nix", "flake", "lock"])

    info("Running the initial hpack...")
    _ = nix_run(["hpack"])

    info("Running fourmolu...")
    _ = nix_run(["fourmolu", "-i", "app", "src"])

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

    if "{{ cookiecutter.executable }}" == "False":
        shutil.rmtree(pathlib.Path("app"))

    if "{{ cookiecutter.library }}" == "False":
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
