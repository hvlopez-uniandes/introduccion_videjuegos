# MISW-4407 — Introducción al desarrollo de videojuegos (ECS)

## Semana 4 (modo por defecto)

Sobre la semana 3 se añade interfaz con fuentes, audio vía **Service Locator**, pausa y una **habilidad especial** con recarga visible.

### Patrón Service Locator

Es un **registro central de servicios**: un solo objeto (`ServiceLocator`) conoce las implementaciones concretas de “cómo cargar recursos”. Los sistemas y utilidades **no** abren archivos de imagen/audio/fuente a pelo con rutas globales sueltas: piden el servicio por nombre y llaman a su API. Así el curso pide **localizar** carga de sonidos, imágenes y texto/fuentes en un solo patrón.

| Pieza | Archivo | Rol |
|--------|---------|-----|
| Registro | `src/engine/service_locator.py` | `ServiceLocator.register(name, service)`, `ServiceLocator.bind(locator)` (instancia global), `ServiceLocator.current().get("…")` |
| Implementaciones | `src/engine/resource_services.py` | **`TextureService`**: `load(ruta_relativa)` → `pygame.Surface` (usa el caché de `textures.py`). **`SoundService`**: `load(ruta)` → `pygame.mixer.Sound` con caché. **`FontService`**: `get(ruta_ttf, tamaño_px)` → `pygame.font.Font` con caché por (ruta, tamaño). |
| Arranque | `GameEngine._bind_services()` en `game_engine.py` | Tras `pygame.init()` / `mixer`, se crea el `ServiceLocator`, se registran los tres servicios con la **raíz del proyecto**, y se llama a `ServiceLocator.bind(...)`. |
| Uso típico | Sistemas / helpers | `ServiceLocator.current().get("textures").load("assets/img/...")`, `.get("sounds").load("assets/snd/...")`, `.get("fonts").get("assets/fnt/....ttf", 12)`. Reproducción cómoda: `src/engine/audio_util.py` → `play_sound(ruta, volumen)` por debajo usa el **SoundService**. |

**Dónde se usa en este proyecto (referencia rápida):** spawner y disparo cargan **texturas** vía `TextureService`; explosiones idem; HUD del escudo pide **fuente** al `FontService` para `font.render` / `CSurface.update_from_text`; todos los **`.ogg`** pasan por `SoundService` (directo o vía `play_sound`). No hace falta pasar el `ServiceLocator` a cada sistema: la instancia global enlazada al inicio basta para cumplir el patrón en un juego pequeño.

### Qué incluye

- **Service Locator**: ver subsección anterior; archivos `service_locator.py` y `resource_services.py`.
- **`interface.json`**: fuente `.ttf`, texto y color del **título**, **instrucciones** en pantalla, estilo del HUD dinámico del pulso y datos del texto de **pausa** (tamaño/color).
- **Texto en pantalla**: entidades HUD con `CTagHud` / `CTagHudDynamic`; `CSurface.from_text` para textos fijos y `update_from_text` para el texto que cambia (recarga del pulso).
- **Pausa**: tecla **P**; con pausa activa no se ejecutan los sistemas de simulación; overlay oscuro y mensaje de pausa (desde `interface.json`).
- **Sonidos** (rutas relativas a la raíz del repo, típicamente bajo `assets/snd/`):
  - **`sound`** en `enemies.json` (asteroides y Hunter al aparecer), **`sound_chase`** solo en Hunter (al pasar de idle a perseguir).
  - **`sound`** en `bullet.json` (al disparar), **`sound`** en `explosion.json` (al crear la entidad explosión en impactos bala–enemigo).
  - **`sound`** en `player.json` → movimiento del personaje (muestreado para no saturar); **`sound_collision`** → choque jugador–enemigo (la explosión visual en ese caso no dispara el sonido de `explosion.json` para no duplicar).
- **Habilidad única — pulso escudo**: entrada **ESPACIO** (configurable); ventana de efecto, eliminación de enemigos en radio, **cooldown** con texto numérico y **porcentaje** de recarga; **anillo** alrededor del jugador mientras está activo. Parámetros en **`special.json`** → `shield_pulse`.

### Recursos

- **Imágenes**: `assets/img/` (como en semanas anteriores).
- **Audio**: `assets/snd/` (p. ej. `laser.ogg`, `explosion.ogg`, `asteroid.ogg`, `ufo.ogg` en el repo de ejemplo).
- **Fuente**: `assets/fnt/PressStart2P.ttf` (referenciada en `interface.json`).

### Config por defecto (`src/cfg/`)

Ocho JSON en la **raíz** de la carpeta:

| Archivo | Rol |
|---------|-----|
| `window.json` | Ventana |
| `enemies.json` | Tipos de enemigo + **`sound`** / Hunter + **`sound_chase`** |
| `level_01.json` | Spawn y jugador |
| `player.json` | Sprite jugador + **`sound`** (movimiento) + **`sound_collision`** |
| `bullet.json` | Bala + **`sound`** |
| `explosion.json` | Explosión + **`sound`** |
| **`interface.json`** | Fuente y textos de UI (título, pausa, ayuda, HUD del pulso) |
| **`special.json`** | `shield_pulse`: `duration_sec`, `cooldown_sec`, `radius_px`, `activation_key` (p. ej. `SPACE`) |

### Cómo probar la Semana 4

1. Instalación como arriba (`venv` + `pip install -r requirements.txt`).
2. Ejecutar: `python3 main.py` (carga `src/cfg/` por defecto).
3. Comprobar:
   - **Service Locator**: al arrancar no hay error de servicios no inicializados; imágenes, `.ogg` y `.ttf` cargan (si falta un archivo, fallará la ruta concreta, no el registro).
   - **Título** e **instrucciones** visibles.
   - **P**: pausa y texto; **P** otra vez reanuda.
   - **Sonidos** al spawn, disparo, explosiones, chase del Hunter, movimiento y choque jugador–enemigo.
   - **ESPACIO**: pulso escudo; línea de estado con recarga; anillo durante el efecto; tras cooldown vuelve a **LISTO**.

### Entrega (curso)

- Publicar el juego en **itch.io** (web o descargable).
- Incluir en el ZIP un **`README.txt`** con el **enlace** al juego. En el repo hay una plantilla en la raíz: reemplazá la URL por la definitiva antes de entregar.

Recursos oficiales del curso (referencia): [recursos semana 4](https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/).

### Rúbrica Semana 4 (resumen)

| Dimensión | Peso | Dónde se nota en el proyecto |
|-----------|------|------------------------------|
| Funcionamiento básico | 10% | `GameEngine`, pygame, bucle estable |
| Sprites y sonidos | 10% | JSON + `TextureService` / `SoundService` |
| Texto y fuentes | 10% | `interface.json`, `FontService`, HUD |
| Pausa | 10% | **P**, `game_state.paused`, overlay |
| Service Locator | 20% | Registro y uso de los tres servicios |
| Característica única | 20% | Pulso escudo + HUD + anillo + `special.json` |
| itch.io | 20% | `README.txt` + publicación (lo completás vos) |

---


## Semana 3 (modo por defecto)

Sobre la semana 2 se añade:

- **Sprites** (`CSurface`): textura PNG y área de colisión/dibujo por fotograma (tira horizontal).
- **`CAnimation`** + **`system_animation`**: clips con nombre, `start`/`end`, `framerate` (desde JSON).
- **Jugador y Hunter**: animaciones **MOVE** e **IDLE**; solo **MOVE** cuando hay movimiento.
- **Hunter** (`CTagHunter` + `CHunterAI` + `system_hunter_ai`): persigue al jugador si está a distancia ≤ `distance_start_chase`; si se aleja más de `distance_start_return` del **origen de spawn**, vuelve a ese punto a `velocity_return` y luego puede volver a perseguir.
- **Asteroides**: mismos rebotes que antes (sin Hunter en `system_bounce`).
- **Explosión** (`CTagExplosion`): entidad aparte al destruirse bala–enemigo o jugador–enemigo; animación **EXPLODE** no en bucle; **`system_explosion_cleanup`** la borra al terminar.

### Config y recursos (ZIP *EJ_ECS_03_VERIFICACION*)

- **Por defecto** el motor usa **`src/cfg/`**. Semana 3 mínimo: seis JSON (`window`, `enemies`, `level_01`, `player`, `bullet`, `explosion`). **Semana 4** suma **`interface.json`** y **`special.json`** (ocho archivos en total en la raíz de `src/cfg/`).
- Las rutas **`image`** en el JSON son relativas a la **raíz del repo** (p. ej. `assets/img/player.png`). Tené esas PNG en **`assets/img/`** o ajustá las rutas en el JSON.
- Podés usar otra carpeta pasándola a `main.py` (por ejemplo la copia del curso en **`assets/week3_cfg/`**).

### Cómo probar la Semana 3

1. **Entorno** (desde la raíz del proyecto, donde está `main.py`):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Recursos**: confirmá que existen los PNG referenciados en `src/cfg/*.json` (típicamente bajo **`assets/img/`**). Si falta alguno, pygame puede fallar al cargar texturas.

3. **Ejecutar** con la config por defecto (`src/cfg`):

   ```bash
   python3 main.py
   ```

4. **Qué comprobar en pantalla** (checklist rápido):

   - El **jugador** se ve como sprite y las animaciones **IDLE** / **MOVE** cambian al moverte con las flechas.
   - **Disparo** con clic izquierdo (bala sprite); **límite** `max_bullets` del nivel.
   - **Asteroides**: movimiento y rebote en bordes.
   - **Hunter**: te persigue cuando estás cerca; si te alejás del punto donde apareció, vuelve a ese punto y luego puede volver a perseguir.
   - **Bala + enemigo** o **jugador + enemigo**: aparece una **explosión** (sprite, animación sin bucle) y desaparece al terminar el clip.

5. **Otra carpeta de config** (misma estructura de archivos):

   ```bash
   python3 main.py assets/week3_cfg
   ```

### Semana 2 (rectángulos de color)

Seguís pudiendo cargar la verificación semana 2 (cinco JSON por subcarpeta `cfg_XX`):

```bash
python3 main.py assets/verification_s02/cfg_00
```

---

## Entrega Semana 2 (referencia)

Proyecto de la **semana 2**: extiende la semana 1 (enemigos con spawn por tiempo, rebote, `window` / `enemies` / `level_01`) con **jugador**, **balas**, **colisiones**, **patrón Command** y configuración ampliada.

**Verificación semana 2:** carpetas **`src/cfg/cfg_00`**, **`cfg_01`**, **`cfg_02`** — cada una con los **cinco** JSON. Copia en **`assets/verification_s02/`**.

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
| **Service Locator**, sonidos, UI (sem. 4) | `ServiceLocator` + `TextureService` / `SoundService` / `FontService`; HUD y escudo en sistemas dedicados |

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

- **Flechas**: mover al jugador (`input_velocity` en `player.json`; diagonal normalizada).
- **Clic izquierdo**: disparar desde el centro del jugador hacia el puntero (`velocity` en `bullet.json`); respeta `max_bullets` del nivel.
- **P**: pausar / reanudar (sem. 4).
- **Espacio** (o la tecla definida en `special.json`): **pulso escudo** cuando el HUD indique que está listo (sem. 4).

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

| Modo | Carpeta de config | Comando |
|------|-------------------|---------|
| **Semana 4** (por defecto: UI, sonido, pausa, pulso escudo) | `src/cfg` (**ocho** JSON en la raíz; ver tabla Semana 4) | `python3 main.py` |
| Solo assets semana 3 (6 JSON, sin `interface` / `special`) | cualquier carpeta con esa estructura | `python3 main.py <ruta>` — si faltan `interface.json` o `special.json`, el motor usa **valores por defecto** para UI y escudo |
| **Semana 2** (rectángulos, cinco JSON por subcarpeta) | `assets/verification_s02/cfg_00` … `cfg_02` | `python3 main.py assets/verification_s02/cfg_00` |

### Verificación semana 2 (`assets/verification_s02`)

Copia del ZIP **EJ_ECS_02_VERIFICACION** (`cfg_00` … `cfg_02`):

```bash
python3 main.py assets/verification_s02/cfg_00
python3 main.py assets/verification_s02/cfg_01
python3 main.py assets/verification_s02/cfg_02
```

Si tenés la estructura semana 2 bajo `src/cfg` (`cfg_00`, `cfg_01`, …):

```bash
python3 main.py src/cfg/cfg_00
```

## Archivos de configuración (por carpeta)

### Semana 3 (`src/cfg` u otra carpeta plana con los mismos nombres)

| Archivo | Contenido |
|---------|-----------|
| `window.json` | Título, tamaño, fondo, framerate |
| `enemies.json` | Tipos: asteroides con `image` + velocidades; **Hunter** con `image`, `animations`, `velocity_chase`, `velocity_return`, `distance_start_chase`, `distance_start_return` |
| `level_01.json` | `player_spawn` (posición + `max_bullets`) y `enemy_spawn_events` |
| `player.json` | Modo sprite: `image`, `number_frames`, `animations` (clips **IDLE** / **MOVE**); `input_velocity` |
| `bullet.json` | Modo sprite: `image`, `number_frames`, `velocity` |
| `explosion.json` | Sprite y animación **EXPLODE** (sin bucle) para colisiones bala–enemigo / jugador–enemigo |

### Semana 4 (misma carpeta `src/cfg`; archivos extra)

| Archivo | Contenido |
|---------|-----------|
| `interface.json` | `font` (.ttf), bloques `title`, `pause`, `instructions`, `shield_status` (texto, `size`, `color` RGB, `position` donde aplica) |
| `special.json` | `shield_pulse`: duración del efecto, cooldown, radio en px, `activation_key` (`SPACE`, `Q`, etc.) |

Campos de audio opcionales en JSON de semana 3: **`sound`** en `player`, `bullet`, `explosion`, entradas de `enemies`; **`sound_collision`** en `player`; **`sound_chase`** en Hunter dentro de `enemies.json`.

### Semana 2 (cinco JSON; sin `explosion.json` ni sprites obligatorios)

| Archivo | Contenido |
|---------|-----------|
| `window.json` | Título, tamaño, fondo, framerate |
| `enemies.json` | Tipos de enemigo (tamaño, color, velocidades) |
| `level_01.json` | `player_spawn` (posición + `max_bullets`) y `enemy_spawn_events` |
| `player.json` | Tamaño, color, `input_velocity` |
| `bullet.json` | Tamaño, color, `velocity` (rapidez constante del proyectil) |

#### Carpetas de ejemplo (semana 2)

| Carpeta | Notas |
|---------|--------|
| `cfg_00` | Spawn de enemigos escalonado; `max_bullets` moderado. |
| `cfg_01` | Varios enemigos en `time: 0`; más `max_bullets`. |
| `cfg_02` | Enemigos más pequeños; `max_bullets: 1` (probar límite). |

## Comportamiento (enunciado)

- El jugador **no sale** de la pantalla (`system_player_bounds`).
- Los enemigos **rebotan** en los bordes; el jugador **no** usa ese rebote. En semana 3 el rebote aplica a **asteroides**, no al Hunter.
- Las balas salen del **centro** del jugador hacia el ratón; si salen de la pantalla sin impacto, se eliminan.
- **Bala + enemigo**: bala y enemigo desaparecen; en semana 3 aparece **explosión** hasta fin de animación.
- **Jugador + enemigo**: desaparece el **enemigo** (el jugador sigue); en semana 3 también **explosión**.
- **Semana 4**: con **pausa**, el estado del juego no avanza; el **pulso escudo** elimina enemigos en radio durante la ventana configurada y luego entra en recarga.

## Estructura relevante

| Ruta | Descripción |
|------|-------------|
| `src/engine/game_engine.py` | Gameloop, eventos (P, pulso), registro del Service Locator, creación de HUD |
| `src/engine/service_locator.py`, `resource_services.py` | Patrón Service Locator (texturas, sonido, fuentes) |
| `src/engine/audio_util.py` | Reproducción de sonidos vía locator |
| `src/engine/game_state.py`, `frame_input.py` | Pausa y petición de habilidad especial |
| `src/engine/config.py` | Carga de todos los JSON (incl. `interface.json`, `special.json`) |
| `src/ecs/commands.py` | Patrón Command (`PlayerLeftCommand`, `PlayerFireCommand`, …) |
| `src/ecs/components/c_input_command.py` | Cola de comandos |
| `src/ecs/components/c_tags.py` | `CTagPlayer`, `CTagEnemy`, `CTagBullet`, `CTagHunter`, `CTagExplosion`, `CTagHud`, `CTagHudDynamic` |
| `src/ecs/components/c_player_sfx.py`, `c_shield_special.py`, `c_ui_text_style.py` | Audio del jugador, pulso escudo, estilo de texto dinámico |
| `src/ecs/systems/system_input_command.py` | Lee teclado/ratón y encola comandos |
| `src/ecs/systems/system_execute_commands.py` | Ejecuta comandos: velocidad del jugador y disparo |
| `src/ecs/systems/system_player_bounds.py` | Límites del jugador |
| `src/ecs/systems/system_bullet_bounds.py` | Elimina balas fuera de pantalla |
| `src/ecs/systems/system_collision_bullet_enemy.py` | Colisión bala–enemigo |
| `src/ecs/systems/system_collision_player_enemy.py` | Colisión jugador–enemigo |
| `src/ecs/components/c_surface.py`, `c_animation.py` | Sprites y clips (semana 3) |
| `src/ecs/systems/system_animation.py` | Avanza fotogramas de animación |
| `src/ecs/systems/system_player_animation.py`, `system_hunter_animation.py` | IDLE / MOVE según movimiento |
| `src/ecs/systems/system_hunter_ai.py` | IA del Hunter |
| `src/ecs/systems/system_explosion_cleanup.py` | Elimina explosiones al terminar el clip |
| `src/ecs/systems/system_draw.py` | Mundo + capa HUD al final |
| `src/ecs/systems/system_draw_shield_ring.py` | Anillo del pulso escudo |
| `src/ecs/systems/system_shield_pulse.py`, `system_shield_hud_refresh.py` | Lógica del especial y texto de recarga |
| `src/ecs/systems/system_player_move_sound.py` | Sonido de movimiento (throttle) |

## Notas técnicas

### ECS y `delta_time`

Spawn de enemigos y movimiento usan **`delta_time`** del reloj de pygame; no hay timers de Python para el spawn.

### Patrón gameloop (`_update`)

Orden actual (sin pausa): input → ejecutar comandos → spawner enemigos → **IA Hunter** → movimiento → límites jugador → rebote enemigos → límites balas → animación (fotogramas) → animación jugador → animación Hunter → **pulso escudo** → colisiones bala–enemigo / jugador–enemigo → limpieza de explosiones → **sonido movimiento jugador** → **HUD recarga escudo**. Con **pausa**, este bloque no se ejecuta; el dibujo y el overlay de pausa sí.

### Patrón Command

El sistema de input **no** mueve al jugador directamente: llena `CInputCommand.command_queue` con objetos `Command` que implementan `execute(ctx)`; `system_execute_commands` recorre la cola y aplica movimiento y disparo.

### Service Locator (sem. 4)

El motor **no** debe usar `ServiceLocator.current()` antes de `GameEngine._bind_services()`. El orden en `_create` es: `pygame.init()` → `mixer` → **`_bind_services()`** → carga de configs y entidades. Detalle del patrón y tabla de servicios: sección **Patrón Service Locator** arriba (Semana 4).
