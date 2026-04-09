# Plan de Implementación - Escape the Dungeon of Doom

## 1. Arquitectura

```
main() → Game.run() [60 FPS]
          │
          ├─▶ SceneManager (pila escenas)
          ├─▶ InputSystem (teclas → acciones)
          └─▶ Escena.Update() → Render()
```

**Ciclo por frame:**
1. Procesar eventos Pygame (QUIT, KEYDOWN/UP)
2. InputSystem → acciones
3. Escena.Update()
4. Escena.Render()

---

## 2. Módulos

### 2.1 core/ - Núcleo

| Módulo | Responsabilidad |
|--------|------------------|
| main.py | Entry point, init Pygame |
| game.py | Game loop, escenas |
| scene.py | Clase base abstracta |
| scene_manager.py | Pila escenas |
| constants.py | Constantes globales |

### 2.2 entities/ - Entidades

| Entidad | Atributos clave |
|---------|----------------|
| Player | health, position, rotation, weapon, armor |
| Enemy | state, patrol_points, detection_radius |
| Item | type, position |
| Weapon | damage_percent, speed |
| Armor | damage_reduction, speed |
| Door | is_open |
| TileMap | tiles[col][row] |

### 2.3 systems/ - Sistemas

| Sistema | API |
|---------|-----|
| InputSystem | get_actions() → dict |
| PhysicsSystem | check_collision(), resolve_move() |
| CombatSystem | calculate_damage(), can_attack() |
| AISystem | update_enemy() |
| CameraSystem | world_to_screen() |

### 2.4 scenes/ - Escenas

| Escena | Transiciones |
|--------|-------------|
| MenuScene | → GameScene |
| GameScene | → Pause / GameOver / Transition |
| PauseScene | → GameScene / Menu |
| GameOverScene | → GameScene |
| VictoryScene | → Menu |
| LevelTransitionScene | → GameScene |

### 2.5 loaders/ - Cargadores

| Loader | Crea |
|--------|------|
| MapLoader | TileMap, Door |
| PatrolLoader | Enemy.patrol |
| EnemyLoader | Enemy |
| ItemLoader | Item, Weapon, Armor |

---

## 3. Flujos

### 3.1 Input

```
KEY → InputSystem → { accion: bool } → Player.move/rotate()
```

### 3.2 Combate

```
attack() → can_attack()? → Raycast → backstab?
    → damage × 1.25 if backstab → Enemy.take_damage()
```

### 3.3 IA

```
Patrol ─dist<detection──▶ Chase
Chase  ─dist>detection×1.5──▶ Patrol
Chase  ─dist<1──▶ Attack
Attack ─▶attack()→Player.damage() (1s cooldown)
```

### 3.4 Carga nivel

```
GameScene(n) → Loaders → Player=entrada → Transition → Play
```

---

## 4. Transiciones

| Trigger | Resultado |
|---------|----------|
| Menu Start | GameScene(1) |
| ESC | PauseScene |
| health<=0 | GameOverScene→restart |
| exit | Transition→GameScene(n+1) |
| level 5 | VictoryScene→Menu |

---

## 5. Archivos

```
src/
├── main.py
├── core/ (game, scene, scene_manager, constants)
├── entities/ (player, enemy, tilemap, item, weapon, armor, door)
├── systems/ (input, physics, combat, ai, camera)
├── scenes/ (menu, game, pause, gameover, victory, transition)
├── loaders/ (map, patrol, enemy, item)
└── utils/

data/maps/, patrols/, enemies/, items/, sprites/, audio/
```

---

## 6. Dependencias

```
Game → SceneManager → scenes
    → InputSystem
    → GameScene → Player, TileMap, Doors, Items, Systems
```

---

## 7. Fases

### Fase 1: Esqueleto
- [ ] constants.py, main.py, Game loop
- [ ] Scene + SceneManager
- [ ] MenuScene

### Fase 2: Movimiento
- [ ] TileMap + MapLoader
- [ ] Player (WASD + flechas)
- [ ] PhysicsSystem, CameraSystem

### Fase 3: Juego
- [ ] GameScene render
- [ ] Door (E)
- [ ] LevelTransition, Pause

### Fase 4: Enemigos
- [ ] Enemy (estados)
- [ ] AISystem
- [ ] Loaders

### Fase 5: Combate
- [ ] CombatSystem
- [ ] Weapon, Armor
- [ ] Equipar (I, J)

### Fase 6: Fin
- [ ] GameOverScene
- [ ] VictoryScene

### Fase 7: Polish
- [ ] AudioSystem
- [ ] Debug (F3)
- [ ] Tests