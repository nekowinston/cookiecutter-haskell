#!/usr/bin/env python
import subprocess
import pathlib

if __name__ == "__main__":
    # only keep the used licenses
    licenses_to_keep = ["CC0-1.0.txt", "{{ cookiecutter.license }}.txt"]
    for f in pathlib.Path("LICENSES").iterdir():
        if f.name not in licenses_to_keep:
            f.unlink()

    # initialize flake.lock and pre-commit-hooks
    _ = subprocess.call(
        [
            "nix",
            "flake",
            "check",
            "--accept-flake-config",
        ]
    )

    # commit
    _ = subprocess.call(["git", "init"])
    _ = subprocess.call(["git", "add", "*"])
    _ = subprocess.call(["git", "commit", "-m", "feat: initial commit"])
