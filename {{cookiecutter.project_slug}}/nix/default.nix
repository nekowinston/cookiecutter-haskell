{ mkDerivation, lib, base, relude }:
mkDerivation {
  pname = "{{ cookiecutter.project_slug }}";
  version = "0.0.1.0";
  src = ../.;
  isLibrary = true;
  isExecutable = true;
  executableHaskellDepends = [ base relude ];
  mainProgram = "{{ cookiecutter.project_slug }}";
  license = lib.getLicenseFromSpdxId "{{ cookiecutter.license }}";
}
