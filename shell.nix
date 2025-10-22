let
  inherit (import "${builtins.getEnv "HOME"}/nix" { }) pkgs;
  customPython = pkgs.home-assistant.python.withPackages (
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
