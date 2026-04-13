import math

import esper

from src.ecs.commands import CommandContext
from src.ecs.components.c_bullet_def import CBulletDef
from src.ecs.components.c_color import CColor
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_input_speed import CPlayerInputSpeed
from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagBullet, CTagPlayer
from src.ecs.components.c_velocity import CVelocity


def system_execute_commands():
    bullet_def = None
    max_bullets = 99
    for _, sp in esper.get_component(CEnemySpawner):
        max_bullets = sp.max_bullets
    for _, bd in esper.get_component(CBulletDef):
        bullet_def = bd
        break
    if bullet_def is None:
        bullet_def = CBulletDef(5, 5, 255, 0, 0, 200)

    n_bullets = len(list(esper.get_component(CTagBullet)))

    for _ent, (inp, vel, pos, size, speed, _tp) in esper.get_components(
        CInputCommand,
        CVelocity,
        CPosition,
        CSize,
        CPlayerInputSpeed,
        CTagPlayer,
    ):
        ctx = CommandContext()
        for c in inp.command_queue:
            c.execute(ctx)

        dx, dy = ctx.dir_x, ctx.dir_y
        if dx != 0 and dy != 0:
            inv = 1.0 / math.sqrt(2.0)
            dx *= inv
            dy *= inv
        vel.vx = dx * speed.pixels_per_second
        vel.vy = dy * speed.pixels_per_second

        if ctx.fire_mx is not None and n_bullets < max_bullets:
            cx = pos.x + size.w / 2.0
            cy = pos.y + size.h / 2.0
            fdx = ctx.fire_mx - cx
            fdy = ctx.fire_my - cy
            dist = math.hypot(fdx, fdy)
            if dist > 1e-6:
                fdx /= dist
                fdy /= dist
                bvx = fdx * bullet_def.velocity
                bvy = fdy * bullet_def.velocity
                bx = cx - bullet_def.w / 2.0
                by = cy - bullet_def.h / 2.0
                be = esper.create_entity()
                esper.add_component(be, CPosition(bx, by))
                esper.add_component(be, CVelocity(bvx, bvy))
                esper.add_component(be, CSize(bullet_def.w, bullet_def.h))
                esper.add_component(be, CColor(bullet_def.r, bullet_def.g, bullet_def.b))
                esper.add_component(be, CTagBullet())
                n_bullets += 1
