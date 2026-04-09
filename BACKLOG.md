# Escape the Dungeon of Doom - Product Backlog

## Phase 1: Esqueleto (Skeleton)
- [ ] **T001**: Create constants.py with screen, tile, and game constants - [Fase 1] [critica] [backlog]
- [ ] **T002**: Create main.py entry point with pygame init - [Fase 1] [critica] [backlog]
- [ ] **T003**: Create game.py with Game class and 60 FPS loop - [Fase 1] [critica] [backlog]
- [ ] **T004**: Create scene.py with Scene base class (abstract) - [Fase 1] [alta] [backlog]
- [ ] **T005**: Create scene_manager.py with SceneManager (stack) - [Fase 1] [alta] [backlog]
- [ ] **T006**: Create MenuScene with Start/Opciones/Salir options - [Fase 1] [alta] [backlog]

## Phase 2: Movimiento (Movement)
- [ ] **T007**: Create tilemap.py with TileMap class (grid) - [Fase 2] [critica] [backlog]
- [ ] **T008**: Create map_loader.py to load CSV maps - [Fase 2] [critica] [backlog]
- [ ] **T009**: Create player.py with Player entity (pos, rotation) - [Fase 2] [critica] [backlog]
- [ ] **T010**: Implement WASD movement in Player - [Fase 2] [critica] [backlog]
- [ ] **T011**: Implement arrow keys rotation in Player - [Fase 2] [critica] [backlog]
- [ ] **T012**: Create input_system.py with InputSystem class - [Fase 2] [critica] [backlog]
- [ ] **T013**: Create physics_system.py with collision detection - [Fase 2] [alta] [backlog]
- [ ] **T014**: Create camera_system.py with Camera (world-to-screen) - [Fase 2] [alta] [backlog]
- [ ] **T015**: Create GameScene render loop - [Fase 2] [alta] [backlog]

## Phase 3: Juego (Game Logic)
- [ ] **T016**: Implement GameScene full render (walls, floor) - [Fase 3] [alta] [backlog]
- [ ] **T017**: Create door.py with Door class (open/close E key) - [Fase 3] [alta] [backlog]
- [ ] **T018**: Create level_transition_scene.py (fade + level name) - [Fase 3] [alta] [backlog]
- [ ] **T019**: Create pause_scene.py (ESC key, resume/options/exit) - [Fase 3] [alta] [backlog]
- [ ] **T020**: Implement level exit detection and transition - [Fase 3] [alta] [backlog]

## Phase 4: Enemigos (Enemies)
- [ ] **T021**: Create enemy.py with Enemy entity - [Fase 4] [critica] [backlog]
- [ ] **T022**: Implement Enemy states (Patrol/Chase/Attack) - [Fase 4] [critica] [backlog]
- [ ] **T023**: Create ai_system.py with AI state machine - [Fase 4] [critica] [backlog]
- [ ] **T024**: Create patrol_loader.py to load patrol points - [Fase 4] [media] [backlog]
- [ ] **T025**: Create enemy_loader.py to create enemies - [Fase 4] [media] [backlog]
- [ ] **T026**: Implement enemy pathfinding and line-of-sight - [Fase 4] [alta] [backlog]
- [ ] **T027**: Implement enemy attack on player (1s cooldown) - [Fase 4] [alta] [backlog]

## Phase 5: Combate (Combat)
- [ ] **T028**: Create combat_system.py with calculate_damage() - [Fase 5] [critica] [backlog]
- [ ] **T029**: Implement backstab bonus (+25% damage) - [Fase 5] [alta] [backlog]
- [ ] **T030**: Create weapon.py with Weapon (damage, speed) - [Fase 5] [alta] [backlog]
- [ ] **T031**: Create armor.py with Armor (damage_reduction) - [Fase 5] [alta] [backlog]
- [ ] **T032**: Create item_loader.py to load items/weapons/armors - [Fase 5] [media] [backlog]
- [ ] **T033**: Implement item pickup (E key) - [Fase 5] [alta] [backlog]
- [ ] **T034**: Implement equipment system (I=tir weapon, J=tir armor) - [Fase 5] [alta] [backlog]
- [ ] **T035**: Implement player attack (Space key) - [Fase 5] [critica] [backlog]
- [ ] **T036**: Implement dodge mechanic (0.3s window) - [Fase 5] [media] [backlog]

## Phase 6: Fin (End Game)
- [ ] **T037**: Create game_over_scene.py (2s delay + restart) - [Fase 6] [alta] [backlog]
- [ ] **T038**: Create victory_scene.py (level 5, 5s + restart) - [Fase 6] [alta] [backlog]
- [ ] **T039**: Implement full game restart (all levels) - [Fase 6] [alta] [backlog]
- [ ] **T040**: Implement health system (player death) - [Fase 6] [critica] [backlog]

## Phase 7: Polish
- [ ] **T041**: Create audio_system.py (music, sfx) - [Fase 7] [media] [backlog]
- [ ] **T042**: Implement background music with loop - [Fase 7] [media] [backlog]
- [ ] **T043**: Create debug overlay (F3 key) - [Fase 7] [baja] [backlog]
- [ ] **T044**: Implement TAB to show health - [Fase 7] [baja] [backlog]
- [ ] **T045**: Create options_scene.py (fullscreen, rotation speed) - [Fase 7] [media] [backlog]
- [ ] **T046**: Write unit tests for core systems (~50% coverage) - [Fase 7] [media] [backlog]
- [ ] **T047**: Implement graceful degradation (missing assets) - [Fase 7] [baja] [backlog]
- [ ] **T048**: Add logging system (INFO level) - [Fase 7] [baja] [backlog]