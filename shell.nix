let
  inherit (import "${builtins.getEnv "HOME"}/nix" { }) pkgs;
  customPython = pkgs.python313.withPackages (
    p: with p; [
      homeassistant-stubs
      aiohttp
      voluptuous
    ]
  );
in
pkgs.mkShellNoCC {
  packages = [
    customPython
  ];
}
