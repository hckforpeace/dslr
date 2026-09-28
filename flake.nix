{
description = "A very basic flake";

inputs = {
nixpkgs.url = "https://channels.nixos.org/nixpkgs-unstable/nixexprs.tar.zst";
};

outputs = inputs: {
devShells = builtins.mapAttrs (system: pkgs: {
default = pkgs.mkShell {
packages = [
pkgs.python312
pkgs.ruff
pkgs.basedpyright
pkgs.prettier
pkgs.uv
pkgs.stdenv.cc.cc
pkgs.zlib
];

    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
    ];
  };
}) inputs.nixpkgs.legacyPackages;

};
}

