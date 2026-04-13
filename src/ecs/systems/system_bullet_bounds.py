import esper

from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagBullet


def system_bullet_bounds(screen_w, screen_h):
    sw = float(screen_w)
    sh = float(screen_h)
    to_kill = []

    for ent, (pos, size, _tb) in esper.get_components(CPosition, CSize, CTagBullet):
        if pos.x + size.w <= 0 or pos.x >= sw or pos.y + size.h <= 0 or pos.y >= sh:
            to_kill.append(ent)

    for ent in to_kill:
        esper.delete_entity(ent, immediate=True)
