#!/usr/bin/python3
# MISW-4407 — Entrega 2 (semana 2: jugador, balas, Command + configs ampliados)

import sys
from pathlib import Path

from src.engine.game_engine import GameEngine

if __name__ == "__main__":
    # Sin argumentos: src/cfg/cfg_00 (semana 2). Verificación:
    #   python3 main.py assets/verification_s02/cfg_01
    #   python3 main.py src/cfg/cfg_01
    cfg_folder = None
    if len(sys.argv) >= 2:
        cfg_folder = Path(sys.argv[1])

    game = GameEngine(cfg_dir=cfg_folder)
    game.run()
