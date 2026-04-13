import math

import esper

from src.ecs.components.c_hunter_ai import CHunterAI
from src.ecs.components.c_position import CPosition
from src.ecs.components.c_tags import CTagHunter, CTagPlayer
from src.ecs.components.c_velocity import CVelocity


def system_hunter_ai():
    players = list(esper.get_components(CPosition, CTagPlayer))
    if not players:
        return
    _, (ppos, _tp) = players[0]

    for _ent, (pos, vel, ai, _th) in esper.get_components(CPosition, CVelocity, CHunterAI, CTagHunter):
        dx_p = ppos.x - pos.x
        dy_p = ppos.y - pos.y
        dist_p = math.hypot(dx_p, dy_p)
        dist_o = math.hypot(pos.x - ai.origin_x, pos.y - ai.origin_y)

        if ai.state == "return":
            dx = ai.origin_x - pos.x
            dy = ai.origin_y - pos.y
            d = math.hypot(dx, dy)
            if d < 2.0:
                pos.x = ai.origin_x
                pos.y = ai.origin_y
                vel.vx = 0.0
                vel.vy = 0.0
                ai.state = "idle"
            else:
                vel.vx = dx / d * ai.v_return
                vel.vy = dy / d * ai.v_return
        elif ai.state == "chase":
            if dist_o > ai.return_dist + 0.5:
                ai.state = "return"
                continue
            if dist_p < 1e-6:
                vel.vx = 0.0
                vel.vy = 0.0
            else:
                vel.vx = dx_p / dist_p * ai.v_chase
                vel.vy = dy_p / dist_p * ai.v_chase
        else:
            vel.vx = 0.0
            vel.vy = 0.0
            if dist_p <= ai.chase_dist:
                ai.state = "chase"
