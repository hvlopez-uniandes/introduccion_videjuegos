import esper

from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize
from src.ecs.components.c_tags import CTagEnemy
from src.ecs.components.c_velocity import CVelocity


def system_bounce(screen_w, screen_h):
    sw = float(screen_w)
    sh = float(screen_h)

    for _entity, (pos, vel, size, _tag) in esper.get_components(CPosition, CVelocity, CSize, CTagEnemy):
        # Límite derecho/abajo: si el rectángulo es más grande que la ventana, max queda en 0
        max_x = max(0.0, sw - float(size.w))
        max_y = max(0.0, sh - float(size.h))

        if pos.x < 0:
            pos.x = 0.0
            vel.vx = abs(vel.vx)
        elif pos.x > max_x:
            pos.x = max_x
            vel.vx = -abs(vel.vx)

        if pos.y < 0:
            pos.y = 0.0
            vel.vy = abs(vel.vy)
        elif pos.y > max_y:
            pos.y = max_y
            vel.vy = -abs(vel.vy)
