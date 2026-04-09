# Prompt de Implementación

Implementa el juego **módulo a módulo**, siguiendo el orden de fases definido en `docs/PLANNING.md`.

## Reglas Generales

1. **Convenciones de código** (de AGENTS.md):
   - Nombres en inglés, snake_case
   - Type hints en funciones públicas
   - Docstrings de una línea (Google style)
   - Usar `pygame.Vector2` para posiciones
   - Dataclasses donde corresponda
   - Constantes en `constants.py`

2. **Estructura de carpetas**: mantener siempre `src/core/`, `src/entities/`, `src/systems/`, `src/scenes/`, `src/loaders/`, `src/utils/`

3. **Nombres de clases**: igual que en PLANNING.md (Game, Scene, Player, Enemy, etc.)

## Orden de Implementación

### Fase 1: Esqueleto
1. `src/core/constants.py` - Todas las constantes
2. `src/core/scene.py` - Clase abstracta
3. `src/core/scene_manager.py` - Pila de escenas
4. `src/core/game.py` - Game loop (60 FPS)
5. `src/main.py` - Entry point
6. `src/scenes/menu_scene.py` - Menú básico

### Fase 2: Movimiento
7. `src/loaders/map_loader.py` - Cargar CSV
8. `src/entities/tilemap.py` - TileMap
9. `src/entities/player.py` - Jugador (movimiento, rotación)
10. `src/systems/input_system.py` - Teclas → acciones
11. `src/systems/physics_system.py` - Colisiones AABB
12. `src/systems/camera_system.py` - Cámara
13. `src/scenes/game_scene.py` - Render

### Fase 3: Juego
14. `src/entities/door.py` - Puertas
15. `src/scenes/level_transition_scene.py` - Transiciones
16. `src/scenes/pause_scene.py` - Pausa

### Fase 4: Enemigos
17. `src/entities/enemy.py` - Enemy con estados
18. `src/loaders/patrol_loader.py` - Cargar patrols
19. `src/loaders/enemy_loader.py` - Cargar enemigos
20. `src/systems/ai_system.py` - IA

### Fase 5: Combate
21. `src/entities/weapon.py` - Armas
22. `src/entities/armor.py` - Armaduras
23. `src/entities/item.py` - Items
24. `src/loaders/item_loader.py` - Cargar items
25. `src/systems/combat_system.py` - Daño, backstab

### Fase 6: Fin
26. `src/scenes/gameover_scene.py` - Derrota
27. `src/scenes/victory_scene.py` - Victoria
28. Lógica de restart completo

### Fase 7: Polish
29. `src/systems/audio_system.py` - Audio (opcional)
30. Tests (~50% cobertura)

## Requisitos por Módulo

Cada módulo debe incluir:
- Docstring de una línea explicando responsabilidad
- Type hints en métodos públicos
- Constantes referenciadas desde `constants.py`
- Logging de errores (no print)

## Reglas de Commit

- Commit após completar cada módulo de la lista
- Mensaje claro: "add: Player movement" (no "trabajo")
- No hacer commit de archivos vacíos o solo con docstrings

## Verificación

Após implementar un módulo:
1. Ejecutar `uv run python -m src.main` para verificar
2. Si hay errores, corregir antes de continuar
3. Mantener el mismo formato y convenciones en todo el código