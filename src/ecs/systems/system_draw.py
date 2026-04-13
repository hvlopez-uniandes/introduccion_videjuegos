import esper
import pygame

from src.ecs.components.c_color import CColor
from src.ecs.components.c_position import CPosition
from src.ecs.components.c_size import CSize


def system_draw(surface):
    for _entity, (pos, size, color) in esper.get_components(CPosition, CSize, CColor):
        rect = pygame.Rect(int(pos.x), int(pos.y), int(size.w), int(size.h))
        pygame.draw.rect(surface, (color.r, color.g, color.b), rect)
