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
    ruff
  ];
}
