# Plan de Implementación - Escape the Dungeon of Doom

## 1. Visión General de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        MAIN (src/main.py)                        │
│                            Entry point                           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GAME LOOP (src/core/game.py)                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ UPDATE  │─▶│ INPUT   │─▶│ PHYSICS │─▶│  RENDER │             │
│  │ 60 FPS  │  │Events   │  │Collision│  │ Draw    │             │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘             │
│       ▲           │            │            │                    │
│       └───────────┴────────────┴────────────┘                    │
│                      (tick循环)                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Módulos y Responsabilidades

### 2.1 `src/main.py`
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Inicializar Pygame | `main()` |
| Crear ventana | `pygame.display.set_mode()` |
| Iniciar Game loop | `game.run()` |

### 2.2 `src/core/` - Núcleo del Juego

#### `game.py` - Game Loop Principal
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Controlar bucle principal | `run()`, `_game_loop()` |
| Gestionar escena activa | `set_scene()`, `get_active_scene()` |
| Controlar FPS y delta time | `_calculate_delta()`, `_handle_fps()` |
| Manejar eventos globales | `_process_events()` |

#### `scene.py` - Base de Escenas
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Interfaz abstracta | `update()`, `render()`, `handle_event()`, `enter()`, `exit()` |

#### `scene_manager.py` - Gestor de Escenas
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Registro de escenas | `register_scene()`, `change_scene()` |
| Transiciones | `push()`, `pop()`, `replace()` |
| Stack de escenas | `_scenes: list[Scene]` |

### 2.3 `src/entities/` - Entidades del Juego

#### `player.py` - Jugador
| Responsabilidad | Atributos | Métodos |
|-----------------|-----------|---------|
| Estado del jugador | `health`, `position`, `rotation`, `weapon`, `armor` | `move()`, `rotate()`, `attack()`, `take_damage()` |
| Equipamiento | `inventory` (arma, armadura) | `equip()`, `unequip()` |

#### `enemy.py` - Enemigo
| Responsabilidad | Atributos | Métodos |
|-----------------|-----------|---------|
| Máquina de estados | `state: PatrolState|ChaseState|AttackState` | `update()`, `change_state()` |
| IA | `patrol_points`, `detection_radius` | `patrol()`, `chase()`, `attack()` |

#### `item.py` - Objeto base
| Responsabilidad | Atributos | Métodos |
|-----------------|-----------|---------|
| Items del mundo | `type`, `position`, `sprite` | `pickup()`, `drop()` |

#### `weapon.py` - Arma
| Responsabilidad | Atributos |
|-----------------|-----------|
| Daño y velocidad | `damage_percent`, `speed_modifier`, `name` |

#### `armor.py` - Armadura
| Responsabilidad | Atributos |
|-----------------|-----------|
| Reducción y velocidad | `damage_reduction`, `speed_modifier`, `name` |

#### `door.py` - Puerta
| Responsabilidad | Atributos | Métodos |
|-----------------|-----------|---------|
| Estado | `is_open`, `is_locked`, `position` | `open()`, `close()`, `toggle()` |

### 2.4 `src/systems/` - Sistemas del Juego

#### `input_system.py` - Gestión de Input
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Procesar teclado | `process_input()`, `_handle_keys()` |
| Mapping teclas→acciones | `key_to_action` dict |
| Buffer de input | `_input_buffer: dict` |

**Eventos generadores:**
- `InputEvent(action: str, value: any)`

#### `physics_system.py` - Física y Colisiones
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Detección AABB | `check_collision()`, `resolve_collision()` |
| Movimiento | `apply_movement()`, `_check_wall_collision()` |
| Mapa de colisiones | `_collision_map: dict` |

#### `ai_system.py` - Inteligencia Artificial
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Máquina de estados | `update_enemy()`, `transition()` |
| Pathfinding simple | `find_path()`, `_bfs()` |
| Detección jugador | `can_see_player()`, `is_in_range()` |

**Estados de Enemigo:**
- `PatrolState`: Seguir patrol_points
- `ChaseState`: Perseguir jugador
- `AttackState`: Atacar jugador

#### `combat_system.py` - Sistema de Combate
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Cálculo de daño | `calculate_damage()`, `apply_backstab()` |
| Ventana de esquiva | `check_dodge_window()` |
| Cooldown de ataque | `can_attack()`, `reset_cooldown()` |

**Fórmula de daño:**
```python
damage = weapon.damage_percent * armor.penetrability
if is_backstab: damage *= 1.25
```

#### `audio_system.py` - Audio
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Reproducir efectos | `play_sound()`, `play_music()` |
| Gestión de volumen | `set_volume()`, `mute()` |
| Pool de canales | `_channels: dict` |

#### `camera_system.py` - Cámara
| Responsabilidad | Métodos/Funciones |
|-----------------|-------------------|
| Seguimiento | `follow()`, `update()` |
| Transformación coord | `world_to_screen()`, `screen_to_world()` |

---

## 3. Flujos de Datos

### 3.1 Flujo Principal del Juego
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Pygame     │────▶│  InputSystem │────▶│  Game Loop   │
│   Events     │     │  (key→action)│     │  (update)    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                      ┌──────────────┐           ▼
                      │   Entities   │◀────────────────────┐
                      │ Player,Enemy │                     │
                      └──────┬───────┘     ┌──────────────┐
                             │            │  PhysicsSystem│
                             │            │  (collision) │
                             ▼            └──────┬───────┘
                      ┌──────────────┐           │
                      │  AISystem    │◀──────────┘
                      │ (states, AI) │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  Render      │
                      │  (draw all)  │
                      └──────────────┘
```

### 3.2 Flujo de Input
```
[Tecla presionada] → Pygame.KEYDOWN event
         │
         ▼
[InputSystem.process_event()]
         │
         ├─▶ WASD → action="move" + direction
         ├─▶ Flechas → action="rotate" + amount
         ├─▶ Espacio → action="attack"
         ├─▶ E → action="interact"
         ├─▶ TAB → action="toggle_health"
         └─▶ ESC → action="pause"
         │
         ▼
[Player/Scene.handle_action(action)]
         │
         ▼
[Actualizar estado]
```

### 3.3 Flujo de Combate
```
[Player ataca (Espacio)]
         │
         ▼
[CombatSystem.can_attack()] ──▶ cooldown check
         │
         ▼
[PhysicsSystem.raycast()] ──▶ línea a enemigo
         │
         ▼
[CombatSystem.is_backstab()] ──▶ posición relativa
         │
         ▼
[CombatSystem.calculate_damage()]
         │
         ▼
[Enemy.take_damage(damage)]
         │
         ▼
[AudioSystem.play("hit")]
```

### 3.4 Flujo de IA Enemiga
```
[Enemy.update()]
         │
         ├─▶ Estado: Patrol ──▶ seguir patrol_points
         │
         ├─▶ Estado: Chase ──▶ perseguir posición jugador
         │
         └─▶ Estado: Attack ──▶ attack() cada 1s
         │
[Detección]
         │
         ├─▶ dist < detection_radius ──▶ transición a Chase
         │
         └─▶ dist < attack_distance ──▶ transición a Attack
```

### 3.5 Flujo de Carga de Nivel
```
[Game.set_scene(GameScene)]
         │
         ▼
[SceneManager.change_scene(LevelScene)]
         │
         ▼
[LevelScene.enter()]
         │
         ├─▶ MapLoader.load("data/maps/level_1.csv")
         ├─▶ PatrolLoader.load("data/patrols/level_1.json")
         ├─▶ EnemyLoader.load("data/enemies/level_1.json")
         ├─▶ ItemLoader.load("data/items/level_1.json")
         ├─▶ SpriteCache.load_tiles()
         └─▶ AudioSystem.play_music("level_1")
         │
         ▼
[Transición: pantalla negra 2s]
         │
         ▼
[Nombre nivel 2s]
         │
         ▼
[Juego activo]
```

---

## 4. Eventos Clave

### 4.1 Escenas (Scenes)
| Escena | Descripción | Transiciones |
|--------|-------------|--------------|
| `MenuScene` | Menú principal | → GameScene (Start) |
| `GameScene` | Juego principal | → GameOverScene (player death), → VictoryScene (level 5 complete), → MenuScene (exit) |
| `PauseScene` | Pausa (overlay) | → GameScene (resume) |
| `GameOverScene` | Muerte | → GameScene (restart) |
| `VictoryScene` | Victoria | → MenuScene (restart) |
| `LevelTransitionScene` | Transición entre niveles | → GameScene (next level) |

### 4.2 Eventos de Input
| Evento | Acción | Handler |
|--------|--------|---------|
| `KEYDOWN: W` | Mover adelante | Player.move(forward) |
| `KEYDOWN: S` | Mover atrás | Player.move(backward) |
| `KEYDOWN: A` | Mover izquierda | Player.move(left) |
| `KEYDOWN: D` | Mover derecha | Player.move(right) |
| `KEYDOWN: LEFT` | Girar izquierda | Player.rotate(-angle) |
| `KEYDOWN: RIGHT` | Girar derecha | Player.rotate(+angle) |
| `KEYDOWN: SPACE` | Atacar | Player.attack() |
| `KEYDOWN: E` | Interactuar | Player.interact() |
| `KEYDOWN: I` | Tirar arma | Player.drop_weapon() |
| `KEYDOWN: J` | Tirar armadura | Player.drop_armor() |
| `KEYDOWN: TAB` | Mostrar vida | HUD.toggle_health() |
| `KEYDOWN: ESC` | Pausa | SceneManager.push(PauseScene) |
| `KEYDOWN: F3` | Debug overlay | Debug.toggle() |

### 4.3 Eventos de Juego
| Evento | Cuándo | Acción |
|--------|--------|--------|
| `PLAYER_DIED` | health <= 0 | GameOverScene 2s → restart |
| `LEVEL_COMPLETED` | jugador en salida | Transition 2s → next level |
| `GAME_VICTORY` | level 5 complete | VictoryScene 5s → restart |
| `ENEMY_DETECTED` | dist < detection | Enemy.change_state(ChaseState) |
| `ENEMY_ATTACK` | cooldown ready + dist < 1 | Enemy.attack() → damage player |
| `ITEM_PICKED` | player en celda item | Player.equip(item) |

### 4.4 Eventos de Audio
| Evento | Trigger |
|--------|---------|
| `MUSIC_PLAY` | Scene.enter() |
| `MUSIC_PAUSE` | PauseScene.enter() |
| `SFX_ATTACK` | Player.attack() |
| `SFX_HIT` | Enemy.take_damage() |
| `SFX_DAMAGE` | Player.take_damage() |
| `SFX_PICKUP` | Player.equip() |
| `SFX_DOOR_OPEN` | Door.open() |
| `SFX_DOOR_CLOSE` | Door.close() |

---

## 5. Ciclo de Juego (Game Loop)

```python
def game_loop(self):
    """Bucle principal a 60 FPS."""
    while self._running:
        delta = self._calculate_delta()
        
        # 1. Procesar eventos
        self._process_events()
        
        # 2. Input (si escena activa)
        if self._active_scene:
            self._active_scene.handle_input(delta)
        
        # 3. Update (si no pausado)
        if self._active_scene and not self._paused:
            self._active_scene.update(delta)
        
        # 4. Render
        if self._active_scene:
            self._active_scene.render(self._screen)
        
        # 5. Flip display
        self._clock.tick(60)
        pygame.display.flip()


def _process_events(self):
    """Procesar eventos de Pygame."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if isinstance(self._active_scene, GameScene):
                    self._scene_manager.push(PauseScene())
        elif event.type == pygame.KEYUP:
            pass  # Fin de acciones continuas
```

---

## 6. Estructura de Archivos Final

```
EscapeTheDungeonOfDoom/
├── data/
│   ├── maps/
│   │   ├── level_1_dungeon.csv
│   │   ├── level_2_castle.csv
│   │   ├── level_3_camp.csv
│   │   ├── level_4_forest.csv
│   │   └── level_5_mountain.csv
│   ├── patrols/
│   ├── enemies/
│   ├── items/
│   ├── sprites/
│   └── audio/
├── src/
│   ├── main.py
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py           # Game loop
│   │   ├── scene.py          # Scene base
│   │   ├── scene_manager.py  # Scene stack
│   │   ├── camera.py         # Camera system
│   │   └── constants.py     # Constants
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── item.py
│   │   ├── weapon.py
│   │   ├── armor.py
│   │   └── door.py
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── input_system.py
│   │   ├── physics_system.py
│   │   ├── ai_system.py
│   │   ├── combat_system.py
│   │   ├── audio_system.py
│   │   └── camera_system.py
│   ├── scenes/
│   │   ├── __init__.py
│   │   ├── menu_scene.py
│   │   ├── game_scene.py
│   │   ├── pause_scene.py
│   │   ├── gameover_scene.py
│   │   └── victory_scene.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── map_loader.py
│   │   ├── patrol_loader.py
│   │   ├── enemy_loader.py
│   │   └── item_loader.py
│   └── utils/
│       ├── __init__.py
│       ├── vector.py
│       └── helpers.py
├── config/
│   ├── config.json
│   └── options.json
├── tests/
├── tools/
├── pyproject.toml
└── README.md
```

---

## 7. Dependencias entre Módulos

```
main.py
  └─▶ Game (core/game.py)
       ├─▶ SceneManager (core/scene_manager.py)
       │    └─▶ Scene (scenes/*.py)
       ├─▶ InputSystem (systems/input_system.py)
       ├─▶ AudioSystem (systems/audio_system.py)
       └─▶ Entities
            ├─▶ Player (entities/player.py)
            ├─▶ Enemy (entities/enemy.py)
            ├─▶ Item (entities/item.py)
            └─▶ Door (entities/door.py)

Loaders (loaders/*.py) ──▶ Entities
     ├─▶ MapLoader ──▶ Door, tilemap
     ├─▶ PatrolLoader ──▶ Enemy.patrol_points
     ├─▶ EnemyLoader ──▶ Enemy.stats
     └─▶ ItemLoader ──▶ Item, Weapon, Armor
```

---

## 8. Checklist de Implementación

- [ ] `main.py` - Entry point
- [ ] `constants.py` - Todas las constantes
- [ ] `Game` - Bucle principal
- [ ] `Scene` - Base class
- [ ] `SceneManager` - Stack de escenas
- [ ] `InputSystem` - Mapping teclado
- [ ] `MenuScene` - Menú principal
- [ ] `MapLoader` - Cargar CSV
- [ ] `Player` - Movimiento y ataque
- [ ] `PhysicsSystem` - Colisiones AABB
- [ ] `Door` - Puertas
- [ ] `GameScene` - Escena principal
- [ ] `Enemy` - Máquina de estados
- [ ] `AISystem` - IA Enemiga
- [ ] `CombatSystem` - Daño y backstab
- [ ] `Weapon`, `Armor` - Items
- [ ] `Item` - Sistema de objetos
- [ ] `PauseScene` - Pausa
- [ ] `GameOverScene` - Derrota
- [ ] `VictoryScene` - Victoria
- [ ] `LevelTransition` - Transiciones
- [ ] `AudioSystem` - Sonido
- [ ] `CameraSystem` - Cámara
- [ ] Tests unitarios
- [ ] Limpieza y refactor
