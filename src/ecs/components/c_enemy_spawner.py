# Componente del spawner: acá guardo lo que saqué del level_01.json
# y una copia del diccionario de enemigos para que el sistema pueda crear rectángulos.


class EnemyTypeDef:
    def __init__(
        self,
        size_x,
        size_y,
        color_r,
        color_g,
        color_b,
        velocity_min,
        velocity_max,
    ):
        self.size_x = size_x
        self.size_y = size_y
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.velocity_min = velocity_min
        self.velocity_max = velocity_max


class EnemySpawnEvent:
    # Un evento = a qué segundo spawnea, qué tipo, dónde, y si ya lo hice
    def __init__(self, time_sec, enemy_type, pos_x, pos_y):
        self.time_sec = time_sec
        self.enemy_type = enemy_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fired = False


class CEnemySpawner:
    def __init__(self, events, enemy_types, max_bullets=99, player_spawn_x=320.0, player_spawn_y=180.0):
        self.accumulated_time = 0.0
        self.events = events
        self.enemy_types = enemy_types
        self.max_bullets = int(max_bullets)
        self.player_spawn_x = float(player_spawn_x)
        self.player_spawn_y = float(player_spawn_y)
