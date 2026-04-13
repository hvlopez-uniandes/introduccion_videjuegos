import esper

from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagPlayer


def system_player_bounds(screen_w, screen_h):
    sw = float(screen_w)
    sh = float(screen_h)

    for _ent, (pos, size, _tp) in esper.get_components(CPosition, CSize, CTagPlayer):
        max_x = max(0.0, sw - float(size.w))
        max_y = max(0.0, sh - float(size.h))
        if pos.x < 0:
            pos.x = 0.0
        elif pos.x > max_x:
            pos.x = max_x
        if pos.y < 0:
            pos.y = 0.0
        elif pos.y > max_y:
            pos.y = max_y
