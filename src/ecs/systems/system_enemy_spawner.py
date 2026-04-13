import math
import random

import esper

from src.ecs.components.c_color import CColor
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagEnemy
from src.ecs.components.c_velocity import CVelocity


def system_enemy_spawner(delta_time):
    for _, spawner in esper.get_component(CEnemySpawner):
        spawner.accumulated_time = spawner.accumulated_time + delta_time

        for ev in spawner.events:
            if ev.fired:
                continue
            if spawner.accumulated_time < ev.time_sec:
                continue

            tipo = spawner.enemy_types.get(ev.enemy_type)
            if tipo is None:
                # tipo raro en el json, lo marco para no volver a intentar
                ev.fired = True
                continue

            # velocidad al azar entre min y max, dirección al azar (ángulo)
            speed = random.uniform(tipo.velocity_min, tipo.velocity_max)
            angle = random.uniform(0, 2 * math.pi)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)

            new_enemy = esper.create_entity()
            esper.add_component(new_enemy, CPosition(ev.pos_x, ev.pos_y))
            esper.add_component(new_enemy, CVelocity(vx, vy))
            esper.add_component(new_enemy, CSize(tipo.size_x, tipo.size_y))
            esper.add_component(new_enemy, CColor(tipo.color_r, tipo.color_g, tipo.color_b))
            esper.add_component(new_enemy, CTagEnemy())

            ev.fired = True
