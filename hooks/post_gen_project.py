#!/usr/bin/env python
import subprocess

if __name__ == "__main__":
    _ = subprocess.call(
        [
            "nix",
            "develop",
            "--accept-flake-config",
            "-command",
            "bash",
            "-c",
            '"reuse download --all"',
        ]
    )

    _ = subprocess.call(["git", "init"])
    _ = subprocess.call(["git", "add", "*"])
    _ = subprocess.call(["git", "commit", "-m", "feat: initial commit"])

