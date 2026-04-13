# Cargo los json acá (no en los sistemas), como dijeron en clase.

import json
from pathlib import Path

from src.ecs.components.c_animation import AnimClip
from src.ecs.components.c_bullet_def import CBulletDef
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemySpawnEvent
from src.ecs.components.c_explosion_config import CExplosionConfig
from src.engine.enemy_defs import AsteroidEnemyDef, HunterEnemyDef


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


def _parse_anim_clips(anim_block, loop_default=True):
    """Devuelve number_frames y dict nombre -> AnimClip."""
    nf = int(anim_block["number_frames"])
    clips = {}
    for item in anim_block["list"]:
        name = str(item["name"])
        loops = loop_default if name.upper() != "EXPLODE" else False
        clips[name] = AnimClip(
            name,
            int(item["start"]),
            int(item["end"]),
            float(item["framerate"]),
            loops=loops,
        )
    return nf, clips


def load_window_config(cfg_dir):
    cfg_dir = Path(cfg_dir)
    data = _read_json(cfg_dir / "window.json")
    if isinstance(data, dict) and "window" in data:
        data = data["window"]

    title = str(data.get("title", "Ventana"))
    w = max(1, int(data["size"]["w"]))
    h = max(1, int(data["size"]["h"]))
    bg = data["bg_color"]
    bg_color = (_clamp_byte(bg["r"]), _clamp_byte(bg["g"]), _clamp_byte(bg["b"]))
    framerate = max(1, int(data["framerate"]))
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
            img = info["image"]
            if "distance_start_chase" in info or "velocity_chase" in info:
                ab = info["animations"]
                nf, clips = _parse_anim_clips(ab, loop_default=True)
                result[str(name)] = HunterEnemyDef(
                    str(img),
                    nf,
                    clips,
                    float(info["velocity_chase"]),
                    float(info["velocity_return"]),
                    float(info["distance_start_chase"]),
                    float(info["distance_start_return"]),
                )
            else:
                vmin = float(info["velocity_min"])
                vmax = float(info["velocity_max"])
                if vmin > vmax:
                    vmin, vmax = vmax, vmin
                result[str(name)] = AsteroidEnemyDef(str(img), vmin, vmax)
        except (KeyError, TypeError, ValueError):
            continue
    return result


def _parse_player_spawn(level_data):
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
        if "image" in data:
            return CBulletDef(
                float(data["velocity"]),
                image_path=str(data["image"]),
                num_frames=1,
            )
        sz = data["size"]
        col = data["color"]
        return CBulletDef(
            float(data["velocity"]),
            None,
            float(sz["x"]),
            float(sz["y"]),
            _clamp_byte(col["r"]),
            _clamp_byte(col["g"]),
            _clamp_byte(col["b"]),
        )
    except (KeyError, TypeError, ValueError, FileNotFoundError):
        return CBulletDef(200, image_path="assets/img/bullet.png", num_frames=1)


def build_player_config(cfg_dir):
    cfg_dir = Path(cfg_dir)
    try:
        data = _read_json(cfg_dir / "player.json")
        if "image" in data:
            ab = data["animations"]
            nf, clips = _parse_anim_clips(ab, loop_default=True)
            return {
                "sprite": True,
                "image": str(data["image"]),
                "number_frames": nf,
                "clips": clips,
                "input_velocity": float(data["input_velocity"]),
            }
        sz = data["size"]
        col = data["color"]
        return {
            "sprite": False,
            "w": float(sz["x"]),
            "h": float(sz["y"]),
            "r": _clamp_byte(col["r"]),
            "g": _clamp_byte(col["g"]),
            "b": _clamp_byte(col["b"]),
            "input_velocity": float(data["input_velocity"]),
        }
    except (KeyError, TypeError, ValueError, FileNotFoundError):
        return {
            "sprite": True,
            "image": "assets/img/player.png",
            "number_frames": 4,
            "clips": {},
            "input_velocity": 100.0,
        }


def build_explosion_config(cfg_dir):
    cfg_dir = Path(cfg_dir)
    try:
        data = _read_json(cfg_dir / "explosion.json")
        ab = data["animations"]
        nf, clips = _parse_anim_clips(ab, loop_default=False)
        return CExplosionConfig(str(data["image"]), nf, clips)
    except (KeyError, TypeError, ValueError, FileNotFoundError):
        nf, clips = _parse_anim_clips(
            {
                "number_frames": 8,
                "list": [{"name": "EXPLODE", "start": 0, "end": 7, "framerate": 16}],
            },
            loop_default=False,
        )
        return CExplosionConfig("assets/img/explosion.png", nf, clips)
