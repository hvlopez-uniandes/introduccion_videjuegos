import esper

from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagBullet, CTagEnemy


def _aabb_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def system_collision_bullet_enemy():
    bullets = []
    for e, (pos, size, _tb) in esper.get_components(CPosition, CSize, CTagBullet):
        bullets.append((e, pos, size))

    enemies = []
    for e, (pos, size, _te) in esper.get_components(CPosition, CSize, CTagEnemy):
        enemies.append((e, pos, size))

    to_remove = set()

    for be, bpos, bsize in bullets:
        if be in to_remove:
            continue
        for ee, epos, esize in enemies:
            if ee in to_remove:
                continue
            if _aabb_overlap(
                bpos.x,
                bpos.y,
                bsize.w,
                bsize.h,
                epos.x,
                epos.y,
                esize.w,
                esize.h,
            ):
                to_remove.add(be)
                to_remove.add(ee)

    for ent in to_remove:
        esper.delete_entity(ent, immediate=True)
