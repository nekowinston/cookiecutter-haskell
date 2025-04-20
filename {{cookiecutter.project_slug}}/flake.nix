# SPDX-FileCopyrightText: {{ cookiecutter.__spdx_text }}
# SPDX-License-Identifier: CC0-1.0

{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.flake-compat.follows = "";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ self, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.git-hooks.flakeModule ];

      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];

      # flake.nixosModules = {
      #   default = self.nixosModules.{{ cookiecutter.project_slug }};
      #   {{ cookiecutter.project_slug }} = import ./nix/modules/nixos.nix { inherit self; };
      # };

      flake.overlays.default = final: prev: {
        {% if cookiecutter.is_executable and not cookiecutter.is_library -%}
        {{ cookiecutter.project_slug }} = final.haskell.lib.justStaticExecutables final.haskellPackages.{{ cookiecutter.project_slug }};
        {%- endif %}

        haskellPackages = prev.haskellPackages.override (old: {
          overrides = final.lib.composeExtensions (old.overrides or (_: _: { })) (
            hFinal: hPrev: {
              {{ cookiecutter.project_slug }} = (final.haskellPackages.callPackage ./nix { }).overrideAttrs {
                src = builtins.path {
                  path = final.nix-gitignore.gitignoreSourcePure ''
                    flake.nix
                    flake.lock
                    nix/*
                  '' ./.;
                  name = "{{ cookiecutter.project_slug }}";
                };
              };
            }
          );
        });
      };

      perSystem =
        {
          config,
          pkgs,
          self',
          system,
          ...
        }:
        {
          _module.args.pkgs = import inputs.nixpkgs {
            inherit system;
            config = { };
            overlays = [ inputs.self.overlays.default ];
          };

          devShells.default = pkgs.haskellPackages.shellFor {
            packages = p: [
              p.{{ cookiecutter.project_slug }}
            ];
            nativeBuildInputs = with pkgs; [
              cabal-install
              cabal2nix # pushd nix && cabal2nix ../. > default.nix && popd
              ghcid
              haskell-language-server
              haskellPackages.implicit-hie
              haskellPackages.retrie
              hlint
              hpack

              {% if cookiecutter.use_reuse -%}
              reuse
              {%- endif %}
              self'.formatter
            ];
            shellHook = config.pre-commit.installationScript;
          };

          formatter = pkgs.nixfmt-rfc-style;

          packages = {
            default = self'.packages.{{ cookiecutter.project_slug }};
            {% if cookiecutter.is_executable and not cookiecutter.is_library -%}
            {{ cookiecutter.project_slug }} = pkgs.{{ cookiecutter.project_slug }};
            {%- else %}
            {{ cookiecutter.project_slug }} = pkgs.haskellPackages.{{ cookiecutter.project_slug }};
            {%- endif %}
          };

          pre-commit.settings.hooks = {
            fourmolu.enable = true;
            hlint.enable = true;
            hpack.enable = true;
            nixfmt-rfc-style = {
              enable = true;
              excludes = [ "nix/default.nix" ];
            };
            {% if cookiecutter.use_reuse -%}
            reuse.enable = true;
            {%- endif %}
          };
        };
    };

  {% if cookiecutter.author_name == "winston" -%}
  nixConfig = {
    extra-substituters = [ "https://attic.winston.sh/public" ];
    extra-trusted-public-keys = [ "public:gqpCDffg2eWolOCakuF0FhU0hmPHvOiBy2Z2rpyf8Mg=" ];
  };
  {%- endif %}
}
