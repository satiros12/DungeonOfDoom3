# AGENTS.md - Escape the Dungeon of Doom

## 1. Descripción del Proyecto

Videojuego de acción en primera persona estilo DOOM medieval. El jugador debe escapar de 5 niveles de mazmorras/escenarios, con mecánicas de sigilo y combate cuerpo a cuerpo.

### 1.1 Niveles
| # | Nombre | Descripción |
|---|--------|-------------|
| 1 | Dungeon | Mazmorra subterránea |
| 2 | Castle | Planta baja del castillo |
| 3 | Camp | Campamento alrededor del castillo |
| 4 | Forest | Bosque amplio |
| 5 | Mountain Pass | Paso de montaña |

### 1.2 Mecánicas Principales
- Movimiento WASD (4 direcciones), mirada con flechas ←→ (rotación horizontal)
- Muerte: Game over 2s + reinicio completo del juego
- Victoria: Completar 5 niveles, pantalla 5s + reinicio
- Transiciones entre niveles: pantalla negra 2s + nombre del nivel 2s
- Mapa de test: sala con items + sala con enemigo configurable

### 1.3 Sistema de Combate
- **Armas**: Puños (10%, 1.0x), Espada (25%, 0.9x), Hacha (40%, 0.7x), Martillo (70%, 0.5x)
- **Armaduras**: Ninguna (1.0x), Ligera (0.75x, 0.8x vel), Media (0.5x, 0.6x vel), Pesada (0.25x, 0.3x vel)
- **Fórmula daño**: `daño = daño_arma × penetrabilidad_armadura`
- **Backstab**: +25% daño al atacar por detrás
- **Ventana de esquiva**: 0.3 segundos
- Ataque: barra espaciadora

### 1.4 Sistema de Enemigos
- Estados: Patrol → Chase → Attack
- Velocidad: 2 celdas/segundo (fija)
- Detección: solo distancia, radio variable por nivel
- Campo de visión: 120°
- Distancia de ataque: 1 celda
- Cooldown de ataque: 1 segundo
- Las paredes bloquean visión y ataque
- Pueden abrir puertas
- Desaparecen al morir

### 1.5 Sistema de Objetos
- 2 armas + 2 armaduras por nivel (niveles 1-3)
- Equipar directo (tira anterior)
- Máximo 1 objeto por celda
- Persisten en nivel, desaparecen al cambiar

### 1.6 UI/HUD
- Menú: Start, Opciones, Salir
- Pausa: ESC → Resume, Opciones, Salir
- Vida oculta (TAB para ver)
- Sin minimapa
- Opciones: Fullscreen, velocidad giro (60-120°/s)

### 1.7 Tecnologías
| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python |
| Framework | Pygame |
| Gestión | UV |
| Sprites | PNG (64x64, horizontal spritesheet) |
| Audio | MP3 (o procedural si no hay) |
| Resolución | 800x600 por defecto |
| Tile | 16px (48x48 mapa) |

### 1.8 Limitaciones
- Sin curación, habilidades, guardado
- Solo un arma + armadura equipadas
- Niveles 4-5 sin objetos
- Sin historia/narrativa
- No hay agacharse

---

## 2. Reglas de Calidad

| Principio | Aplicación |
|-----------|------------|
| **SOLID** | Diseño orientado a componentes |
| **DRY** | Extraer lógica compartida |
| **YAGNI** | Solo lo necesario |
| **SRP** | Una responsabilidad por clase |
| **Nombres** | snake_case en inglés |
| **Comentarios** | Una línea por función (docstring) |

---

## 3. Controles

| Tecla | Acción |
|-------|--------|
| WASD | Moverse |
| ← → | Girar vista |
| Espacio | Atacar |
| E | Recoger/Abrir |
| I | Tirar arma |
| J | Tirar armadura |
| TAB | Mostrar vida |
| ESC | Menú/Pausa |
| F3 | Debug overlay |

---

## 4. Estructura del Proyecto

```
/data
  /maps/          # CSV (48x48)
  /patrols/       # JSON
  /enemies/       # JSON
  /items/         # JSON
  /sprites/      # PNG
  /audio/        # MP3

/src
  /core/         # Game, Scene, Camera
  /components/   # Reusable components
  /entities/     # Player, Enemy, Item, Door
  /systems/     # Input, Physics, AI, Combat, Audio
  /utils/       # Constants, helpers

/config          # config.json, options.json
```

### 4.1 Formato Mapas CSV
- `_`: vacío, `#`: pared, `P`: entrada, `E`: salida (2 celdas)
- `D`: puerta, `0-9`: enemigo, `a-z`: objeto, `.`: decorado

### 4.2 Colores por Defecto
| Entidad | Color |
|---------|-------|
| Jugador | Verde |
| Enemigo | Rojo |
| Puerta | Azul |
| Objeto | Amarillo |
| Pared | Gris |
| Decorado | Marrón |
| Salida | Dorado |

---

## 5. Comandos

```bash
uv run python -m src.main   # Ejecutar
uv run pytest              # Tests
uv run pylint src/         # Linting
python tools/generate_map.py
```

---

## 6. Arquitectura de Código

### 6.1 Patrón
ECS-like (Entity + Components)

### 6.2 Clases Principales
- `Game` - Game loop principal
- `Scene` / `SceneManager` - Menú, Juego, Game Over
- `Player` - Entidad del jugador
- `Enemy` - IA con estados (PatrolState, ChaseState, AttackState)
- `Item`, `Weapon`, `Armor` - Sistema de items
- `Door` - Puertas con animación
- `Camera` - Seguimiento del jugador

### 6.3 Sistemas
- `InputSystem` - Procesa teclado
- `PhysicsSystem` - Movimiento y colisiones (AABB)
- `AISystem` - Máquina de estados
- `CombatSystem` - Daño y backstab
- `AudioSystem` - Sonido y música

### 6.4 Configuración
- `config.json` - General (versión, paths, constantes)
- `options.json` - Opciones (volumen, fullscreen, velocidad giro)

---

## 7. Convenciones de Código

- Type hints en funciones públicas
- Google style docstrings
- dataclasses donde apropiado
- pygame.Vector2 para posiciones
- Constantes en `constants.py` (SCREEN_WIDTH, TILE_SIZE, etc.)
- Logging INFO + archivo
- Tests con pytest (~50-70% cobertura)
- ruff para formateo
- pylint score > 8

---

## 8. Notas de Implementación

- Cargar sprites lazy, cache en memoria
- 60 FPS con vsync
- Graceful degradation si faltan assets
- Excepciones con logging
- Transiciones con fade (0.5s)
- Música con loop, se pausa con el juego
- Debug overlay con F3
