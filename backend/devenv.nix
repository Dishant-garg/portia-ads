{ pkgs, lib, config, ... }: {
  languages.python.enable = true;
  languages.python.uv.enable = true;

  packages = with pkgs; [
    python313
    python313Packages.uvicorn

    ninja
    pkg-config
    
  ];

 
  enterShell = ''
    if [ -z "$ZSH_VERSION" ]; then
      exec zsh
    fi

    uv sync
  '';
}