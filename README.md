# MISW-4407 — Entrega Semana 2 (ECS)

Proyecto de la **semana 2**: extiende la semana 1 (enemigos con spawn por tiempo, rebote, `window` / `enemies` / `level_01`) con **jugador**, **balas**, **colisiones**, **patrón Command** y configuración ampliada.

**Verificación:** carpetas **`src/cfg/cfg_00`**, **`cfg_01`**, **`cfg_02`** — cada una con los **cinco** JSON. Debe coincidir con pegar el contenido del ZIP del curso (p. ej. *EJ_ECS_02_VERIFICACION* en la web de la materia). Copia adicional en **`assets/verification_s02/`**.

---

## Detalles de configuración (enunciado Semana 2)

| Origen | Qué define |
|--------|------------|
| **Nivel (`level_01.json`)** | Origen del jugador (`player_spawn.position`), máximo de balas en pantalla (`player_spawn.max_bullets`), más `enemy_spawn_events` (tiempos y tipos como en semana 1). |
| **Jugador (`player.json`)** | Tamaño (`size`), color, **velocidad de entrada** (`input_velocity`, píxeles por segundo con teclado). |
| **Bala (`bullet.json`)** | Tamaño, color, **velocidad de disparo constante** (`velocity`). |
| **Resto** | `window.json`, `enemies.json` como en módulos anteriores. |

---

## Detalles de implementación (checklist frente al código)

| Recomendación del curso | Implementación |
|-------------------------|----------------|
| **`CInputCommand`** | `src/ecs/components/c_input_command.py` — cola de comandos por frame. |
| **`CTagPlayer`**, **`CTagBullet`**, **`CTagEnemy`** | `src/ecs/components/c_tags.py` |
| Sistema input + **patrón Command** | `system_input_command` encola; `system_execute_commands` ejecuta. Acciones: **PLAYER_LEFT/RIGHT/UP/DOWN** (clases en `commands.py`) y **PLAYER_FIRE** (`PlayerFireCommand`). |
| Límites del **jugador** | `system_player_bounds` |
| Límites de **balas** (fuera de pantalla → borrar) | `system_bullet_bounds` |
| Colisión **jugador–enemigo** | `system_collision_player_enemy` |
| Colisión **bala–enemigo** | `system_collision_bullet_enemy` |
| JSON solo fuera de sistemas de juego principal | Carga en `src/engine/config.py` y `GameEngine._create()`. |

---

## Rúbrica Semana 2 (pesos del curso)

| Dimensión | Peso | Qué revisa el proyecto |
|-----------|------|-------------------------|
| **Funcionamiento básico** | 15% | `GameEngine` + pygame; flechas, clic, colisiones sin errores de ejecución con los configs de ejemplo. |
| **Sistema de movimiento del usuario** | 20% | Flechas mueven al jugador según `input_velocity`; diagonal normalizada (misma rapidez en diagonal). |
| **Sistema de movimiento de la bala** | 20% | Bala desde el **centro** del jugador hacia el ratón; rapidez constante (`bullet.json`); desaparece en bordes; respeta **`max_bullets`**. |
| **Patrón Command simplificado** | 15% | Comandos como objetos con `execute(ctx)`; input no aplica movimiento/disparo directamente. |
| **Sistemas anteriores** | 10% | Spawner enemigos con `delta_time`, tipos desde `enemies.json`, movimiento + rebote solo enemigos, dibujo ECS, gameloop claro. |
| **Elementos extra de configuración** | 20% | Uso de los **cinco** archivos y de **todas** las carpetas de ejemplo (`cfg_00` … `cfg_02`). |

*(Los niveles Deficiente / Regular / Muy bien / Excelente son los del documento oficial del curso; este README indica dónde está cada dimensión en el código.)*

---

## Controles

- **Flechas**: mover el rectángulo del jugador (velocidad `input_velocity` en `player.json`, píxeles por segundo; diagonal normalizada).
- **Clic izquierdo**: disparar bala desde el **centro** del jugador hacia el puntero (velocidad constante `velocity` en `bullet.json`). Respeta `max_bullets` del nivel.

## Requisitos

- Python **3.9** o superior (recomendado).
- Entorno virtual opcional pero aconsejable.

## Instalación

Desde la **raíz del proyecto** (donde está `main.py`):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo ejecutar

Por defecto: **`src/cfg/cfg_00`** (semana 2, cinco JSON por carpeta).

```bash
python3 main.py
```

### Verificación semana 2 (`assets/verification_s02`)

Copia del ZIP **EJ_ECS_02_VERIFICACION** (`cfg_00` … `cfg_02`):

```bash
python3 main.py assets/verification_s02/cfg_00
python3 main.py assets/verification_s02/cfg_01
python3 main.py assets/verification_s02/cfg_02
```

### Copia bajo `src/cfg`

```bash
python3 main.py src/cfg/cfg_01
```

## Archivos de configuración (por carpeta)

| Archivo | Contenido |
|---------|-----------|
| `window.json` | Título, tamaño, fondo, framerate |
| `enemies.json` | Tipos de enemigo (tamaño, color, velocidades) |
| `level_01.json` | `player_spawn` (posición + `max_bullets`) y `enemy_spawn_events` |
| `player.json` | Tamaño, color, `input_velocity` |
| `bullet.json` | Tamaño, color, `velocity` (rapidez constante del proyectil) |

### Carpetas de ejemplo (semana 2)

| Carpeta | Notas |
|---------|--------|
| `cfg_00` | Spawn de enemigos escalonado; `max_bullets` moderado. |
| `cfg_01` | Varios enemigos en `time: 0`; más `max_bullets`. |
| `cfg_02` | Enemigos más pequeños; `max_bullets: 1` (probar límite). |

## Comportamiento (enunciado)

- El jugador **no sale** de la pantalla (`system_player_bounds`).
- Los enemigos **rebotan** en los bordes; el jugador **no** usa ese rebote.
- Las balas salen del **centro** del jugador hacia el ratón; si salen de la pantalla sin impacto, se eliminan.
- **Bala + enemigo**: ambos desaparecen.
- **Jugador + enemigo**: desaparece el **enemigo** (el jugador sigue).

## Estructura relevante

| Ruta | Descripción |
|------|-------------|
| `src/engine/game_engine.py` | Gameloop y orden de sistemas |
| `src/engine/config.py` | Carga de todos los JSON |
| `src/ecs/commands.py` | Patrón Command (`PlayerLeftCommand`, `PlayerFireCommand`, …) |
| `src/ecs/components/c_input_command.py` | Cola de comandos |
| `src/ecs/components/c_tags.py` | `CTagPlayer`, `CTagEnemy`, `CTagBullet` |
| `src/ecs/systems/system_input_command.py` | Lee teclado/ratón y encola comandos |
| `src/ecs/systems/system_execute_commands.py` | Ejecuta comandos: velocidad del jugador y disparo |
| `src/ecs/systems/system_player_bounds.py` | Límites del jugador |
| `src/ecs/systems/system_bullet_bounds.py` | Elimina balas fuera de pantalla |
| `src/ecs/systems/system_collision_bullet_enemy.py` | Colisión bala–enemigo |
| `src/ecs/systems/system_collision_player_enemy.py` | Colisión jugador–enemigo |

## Notas técnicas

### ECS y `delta_time`

Spawn de enemigos y movimiento usan **`delta_time`** del reloj de pygame; no hay timers de Python para el spawn.

### Patrón gameloop (`_update`)

Orden actual: input → ejecutar comandos → spawner enemigos → movimiento → límites jugador → rebote enemigos → límites balas → colisiones bala–enemigo → colisión jugador–enemigo.

### Patrón Command

El sistema de input **no** mueve al jugador directamente: llena `CInputCommand.command_queue` con objetos `Command` que implementan `execute(ctx)`; `system_execute_commands` recorre la cola y aplica movimiento y disparo.
# introduccion_videjuegos
