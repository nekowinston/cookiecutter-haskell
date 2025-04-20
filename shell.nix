# SPDX-FileCopyrightText: 2025 winston <hey@winston.sh>
# SPDX-License-Identifier: CC0-1.0

{
  pkgs ? import <nixpkgs> {
    config = { };
    overlays = [ ];
  },
}:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    (python3.withPackages (p: [ p.cookiecutter ]))
    basedpyright
    reuse
    ruff
  ];
}
