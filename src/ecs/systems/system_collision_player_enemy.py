import esper

from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagEnemy, CTagPlayer


def _aabb_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def system_collision_player_enemy():
    players = list(esper.get_components(CPosition, CSize, CTagPlayer))
    if not players:
        return

    _pe, (ppos, psize, _tp) = players[0]

    to_remove = []
    for ee, (epos, esize, _te) in esper.get_components(CPosition, CSize, CTagEnemy):
        if _aabb_overlap(
            ppos.x,
            ppos.y,
            psize.w,
            psize.h,
            epos.x,
            epos.y,
            esize.w,
            esize.h,
        ):
            to_remove.append(ee)

    for ent in to_remove:
        esper.delete_entity(ent, immediate=True)
