from pathlib import Path

import esper
import pygame

from src.engine.config import (
    build_bullet_def,
    build_enemy_spawner_component,
    build_enemy_type_defs,
    build_explosion_config,
    build_player_config,
    load_window_config,
)
from src.engine.paths import set_project_root
from src.engine.textures import clear_texture_cache, load_texture
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_color import CColor
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_input_speed import CPlayerInputSpeed
from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tags import CTagPlayer
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.system_animation import system_animation
from src.ecs.systems.system_bounce import system_bounce
from src.ecs.systems.system_bullet_bounds import system_bullet_bounds
from src.ecs.systems.system_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.system_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.system_draw import system_draw
from src.ecs.systems.system_enemy_spawner import system_enemy_spawner
from src.ecs.systems.system_execute_commands import system_execute_commands
from src.ecs.systems.system_explosion_cleanup import system_explosion_cleanup
from src.ecs.systems.system_hunter_ai import system_hunter_ai
from src.ecs.systems.system_hunter_animation import system_hunter_animation
from src.ecs.systems.system_input_command import system_input_command
from src.ecs.systems.system_movement import system_movement
from src.ecs.systems.system_player_animation import system_player_animation
from src.ecs.systems.system_player_bounds import system_player_bounds


class GameEngine:
    def __init__(self, cfg_dir=None):
        self._root = Path(__file__).resolve().parents[2]
        if cfg_dir is None:
            self._cfg_dir = self._root / "src" / "cfg"
        else:
            self._cfg_dir = Path(cfg_dir)
            if not self._cfg_dir.is_absolute():
                self._cfg_dir = (self._root / self._cfg_dir).resolve()

        self.is_running = False
        self.delta_time = 0.0

        self.screen = None
        self.clock = None
        self.framerate = 60
        self.bg_color = (0, 0, 0)
        self.screen_w = 640
        self.screen_h = 360

    def run(self):
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        clear_texture_cache()
        esper.clear_database()
        pygame.init()
        set_project_root(self._root)

        title, w, h, self.bg_color, self.framerate = load_window_config(self._cfg_dir)
        self.screen_w = w
        self.screen_h = h

        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()

        enemy_types = build_enemy_type_defs(self._cfg_dir)
        spawner_component = build_enemy_spawner_component(self._cfg_dir, enemy_types)
        bullet_def = build_bullet_def(self._cfg_dir)
        player_cfg = build_player_config(self._cfg_dir)
        explosion_cfg = build_explosion_config(self._cfg_dir)

        entity_spawner = esper.create_entity()
        esper.add_component(entity_spawner, spawner_component)
        esper.add_component(entity_spawner, bullet_def)
        esper.add_component(entity_spawner, explosion_cfg)

        player_entity = esper.create_entity()
        esper.add_component(
            player_entity,
            CPosition(spawner_component.player_spawn_x, spawner_component.player_spawn_y),
        )
        esper.add_component(player_entity, CVelocity(0.0, 0.0))
        esper.add_component(player_entity, CInputCommand())
        esper.add_component(player_entity, CPlayerInputSpeed(player_cfg["input_velocity"]))
        esper.add_component(player_entity, CTagPlayer())

        if player_cfg.get("sprite"):
            psurf = load_texture(self._root, player_cfg["image"])
            pcs = CSurface(psurf, player_cfg["number_frames"])
            panim = CAnimation(player_cfg["number_frames"], player_cfg["clips"], initial="IDLE")
            esper.add_component(player_entity, pcs)
            esper.add_component(player_entity, panim)
        else:
            esper.add_component(player_entity, CSize(player_cfg["w"], player_cfg["h"]))
            esper.add_component(
                player_entity,
                CColor(player_cfg["r"], player_cfg["g"], player_cfg["b"]),
            )

    def _calculate_time(self):
        ms = self.clock.tick(self.framerate)
        self.delta_time = ms / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_input_command()
        system_execute_commands()
        system_enemy_spawner(self.delta_time)
        system_hunter_ai()
        system_movement(self.delta_time)
        system_player_bounds(self.screen_w, self.screen_h)
        system_bounce(self.screen_w, self.screen_h)
        system_bullet_bounds(self.screen_w, self.screen_h)
        system_animation(self.delta_time)
        system_player_animation()
        system_hunter_animation()
        system_collision_bullet_enemy()
        system_collision_player_enemy()
        system_explosion_cleanup()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_draw(self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
