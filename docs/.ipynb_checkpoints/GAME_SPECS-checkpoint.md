# Escape the Dungeon of Doom - Especificaciones Técnicas

## 1. Sistema de Combate

### Armas

| Nombre | Daño Base (%) | Multiplicador de Velocidad |
|--------|---------------|----------------------------|
| Puños | 10 | 1.0 |
| Espada | 25 | 0.9 |
| Hacha | 40 | 0.7 |
| Martillo | 70 | 0.5 |

### Armaduras

| Nombre | Multiplicador de Daño (Penetrabilidad) | Multiplicador de Velocidad |
|--------|------------------------------------------|----------------------------|
| Ninguna | 1.0 | 1.0 |
| Ligera | 0.75 | 0.8 |
| Media | 0.5 | 0.6 |
| Pesada | 0.25 | 0.3 |

### Fórmula de Daño

```
daño_final = daño_arma × penetrabilidad_armadura
```

### Mecánicas Adicionales

- **Backstab**: +25% de daño cuando el jugador ataca por detrás del enemigo
- **Ventana de esquiva**: 0.3 segundos (tiempo durante el cual el jugador puede evitar un ataque)

---

## 2. Sistema de Enemigos

### Estados de IA

1. **Patrol**: Seguimiento de puntos de patrulla predefinidos
2. **Chase**: Persecución activa del jugador (activado al detectar)
3. **Attack**: Ataque al jugador en rango

### Parámetros de Movimiento

| Parámetro | Valor |
|-----------|-------|
| Velocidad de persecución | 2 celdas/segundo |
| Radio de detección | Variable por nivel (ver sección 3) |
| Campo de visión | 120° |
| Distancia de ataque | 1 celda |

### Parámetros de Combate Enemigo

| Parámetro | Valor |
|-----------|-------|
| Cooldown de ataque | 1 segundo |
| Daño base al jugador | 10% de la vida máxima |

---

## 3. Configuración de Niveles

### Radios de Detección por Nivel

| Nivel | Nombre | Radio de Detección (celdas) |
|-------|--------|------------------------------|
| 1 | Dungeon | 5 |
| 2 | Castle | 6 |
| 3 | Camp | 7 |
| 4 | Forest | 8 |
| 5 | Mountain Pass | 9 |

---

## 4. Sistema de Items

### Distribución por Nivel

| Rango de Niveles | Armas | Armaduras |
|-----------------|-------|-----------|
| Niveles 1-3 | 2 armas | 2 armaduras |
| Niveles 4-5 | 0 (sin objetos) | 0 (sin objetos) |

### Notas de Implementación

- Los items aparecen directamente en el nivel
- Al equipar un nuevo item, el anterior se desecha
- No hay sistema de curación ni inventario

---

## 5. Constantes para constants.py

```python
# ==================== ARMAS ====================
WEAPONS = {
    "fists": {"damage_percent": 10, "speed_multiplier": 1.0},
    "sword": {"damage_percent": 25, "speed_multiplier": 0.9},
    "axe": {"damage_percent": 40, "speed_multiplier": 0.7},
    "hammer": {"damage_percent": 70, "speed_multiplier": 0.5},
}

# ==================== ARMADURAS ====================
ARMORS = {
    "none": {"damage_reduction": 1.0, "speed_multiplier": 1.0},
    "light": {"damage_reduction": 0.75, "speed_multiplier": 0.8},
    "medium": {"damage_reduction": 0.5, "speed_multiplier": 0.6},
    "heavy": {"damage_reduction": 0.25, "speed_multiplier": 0.3},
}

# ==================== COMBATE ====================
BACKSTAB_DAMAGE_BONUS = 0.25  # +25% daño por detrás
DODGE_WINDOW = 0.3  # segundos

# ==================== ENEMIGOS ====================
ENEMY_STATES = {
    "PATROL": "patrol",
    "CHASE": "chase",
    "ATTACK": "attack",
}

ENEMY_SPEED = 2.0  # celdas/segundo
ENEMY_FOV = 120  # grados
ENEMY_ATTACK_RANGE = 1  # celda
ENEMY_ATTACK_COOLDOWN = 1.0  # segundos
ENEMY_DAMAGE_TO_PLAYER = 0.1  # 10% de vida

# ==================== NIVELES ====================
LEVELS = {
    1: {"name": "Dungeon", "detection_radius": 5},
    2: {"name": "Castle", "detection_radius": 6},
    3: {"name": "Camp", "detection_radius": 7},
    4: {"name": "Forest", "detection_radius": 8},
    5: {"name": "Mountain Pass", "detection_radius": 9},
}

# ==================== ITEMS POR NIVEL ====================
ITEMS_PER_LEVEL = {
    1: {"weapons": 2, "armors": 2},
    2: {"weapons": 2, "armors": 2},
    3: {"weapons": 2, "armors": 2},
    4: {"weapons": 0, "armors": 0},
    5: {"weapons": 0, "armors": 0},
}
```

---

## 6. Resumen de Controles

| Tecla | Acción |
|-------|--------|
| WASD | Moverse |
| ← → | Girar |
| Espacio | Atacar |
| E | Interactuar |
| I | Tirar arma |
| J | Tirar armadura |
| TAB | Ver vida |

---

## 7. Notas de Diseño

- **Sin curación**: El juego no incluye ningún sistema de curación
- **Sin habilidades**: Solo ataques cuerpo a cuerpo básicos
- **Sin guardado**: Partida única sin opción de guardar/cargar
- **Un solo equipo**: Solo un arma y una armadura equipados simultáneamente
- **Sin narrativa**: Juego puramente de habilidad y supervivencia