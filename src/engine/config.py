# Cargo los json acá (no en los sistemas), como dijeron en clase.

import json
from pathlib import Path

from src.ecs.components.c_bullet_def import CBulletDef
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemySpawnEvent, EnemyTypeDef


def _read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _clamp_byte(n):
    n = int(n)
    if n < 0:
        return 0
    if n > 255:
        return 255
    return n


def load_window_config(cfg_dir):
    """Devuelve título, ancho, alto, color fondo (tupla rgb), framerate."""
    cfg_dir = Path(cfg_dir)
    data = _read_json(cfg_dir / "window.json")
    # Por si el json viene envuelto en "window" (vi los dos formatos en ejemplos)
    if isinstance(data, dict) and "window" in data:
        data = data["window"]

    title = str(data.get("title", "Ventana"))

    w = int(data["size"]["w"])
    h = int(data["size"]["h"])
    # pygame necesita tamaño mínimo razonable
    w = max(1, w)
    h = max(1, h)

    bg = data["bg_color"]
    bg_color = (
        _clamp_byte(bg["r"]),
        _clamp_byte(bg["g"]),
        _clamp_byte(bg["b"]),
    )

    framerate = int(data["framerate"])
    # tick(0) rompe o se comporta mal; aceptamos el json pero lo hacemos válido
    framerate = max(1, framerate)

    return title, w, h, bg_color, framerate


def build_enemy_type_defs(cfg_dir):
    cfg_dir = Path(cfg_dir)
    data = _read_json(cfg_dir / "enemies.json")
    result = {}
    if not isinstance(data, dict):
        return result

    for name, info in data.items():
        if not isinstance(info, dict):
            continue
        try:
            sz = info["size"]
            col = info["color"]
            vmin = float(info["velocity_min"])
            vmax = float(info["velocity_max"])
            if vmin > vmax:
                vmin, vmax = vmax, vmin
            result[str(name)] = EnemyTypeDef(
                float(sz["x"]),
                float(sz["y"]),
                _clamp_byte(col["r"]),
                _clamp_byte(col["g"]),
                _clamp_byte(col["b"]),
                vmin,
                vmax,
            )
        except (KeyError, TypeError, ValueError):
            continue

    return result


def _parse_player_spawn(level_data):
    """Extrae spawn y max_bullets del level_01 (semana 2)."""
    default_x, default_y = 320.0, 180.0
    max_bullets = 99
    if not isinstance(level_data, dict):
        return max_bullets, default_x, default_y
    ps = level_data.get("player_spawn")
    if not isinstance(ps, dict):
        return max_bullets, default_x, default_y
    try:
        pos = ps["position"]
        default_x = float(pos["x"])
        default_y = float(pos["y"])
        max_bullets = int(ps["max_bullets"])
    except (KeyError, TypeError, ValueError):
        pass
    return max(0, max_bullets), default_x, default_y


def build_enemy_spawner_component(cfg_dir, enemy_types):
    cfg_dir = Path(cfg_dir)
    level_data = _read_json(cfg_dir / "level_01.json")
    events = []

    max_bullets, px, py = _parse_player_spawn(level_data)

    if not isinstance(level_data, dict):
        return CEnemySpawner(events, enemy_types, max_bullets, px, py)

    raw_list = level_data.get("enemy_spawn_events", [])
    if not isinstance(raw_list, list):
        return CEnemySpawner(events, enemy_types, max_bullets, px, py)

    for item in raw_list:
        if not isinstance(item, dict):
            continue
        try:
            pos = item["position"]
            events.append(
                EnemySpawnEvent(
                    float(item["time"]),
                    str(item["enemy_type"]),
                    float(pos["x"]),
                    float(pos["y"]),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue

    return CEnemySpawner(events, enemy_types, max_bullets, px, py)


def build_bullet_def(cfg_dir):
    cfg_dir = Path(cfg_dir)
    try:
        data = _read_json(cfg_dir / "bullet.json")
        sz = data["size"]
        col = data["color"]
        return CBulletDef(
            float(sz["x"]),
            float(sz["y"]),
            _clamp_byte(col["r"]),
            _clamp_byte(col["g"]),
            _clamp_byte(col["b"]),
            float(data["velocity"]),
        )
    except (KeyError, TypeError, ValueError, FileNotFoundError):
        return CBulletDef(5, 5, 255, 0, 0, 200)


def build_player_config(cfg_dir):
    """Tamaño, color e input_velocity desde player.json."""
    cfg_dir = Path(cfg_dir)
    try:
        data = _read_json(cfg_dir / "player.json")
        sz = data["size"]
        col = data["color"]
        return {
            "w": float(sz["x"]),
            "h": float(sz["y"]),
            "r": _clamp_byte(col["r"]),
            "g": _clamp_byte(col["g"]),
            "b": _clamp_byte(col["b"]),
            "input_velocity": float(data["input_velocity"]),
        }
    except (KeyError, TypeError, ValueError, FileNotFoundError):
        return {
            "w": 25.0,
            "h": 25.0,
            "r": 200,
            "g": 200,
            "b": 200,
            "input_velocity": 100.0,
        }
