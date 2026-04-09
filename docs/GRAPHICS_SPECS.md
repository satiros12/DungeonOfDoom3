# Especificaciones Gráficas - Escape the Dungeon of Doom

## 1. Paleta de Colores por Entidad

| Entidad | Color (RGB) | Hexadecimal | Descripción |
|---------|-------------|-------------|-------------|
| Jugador | (0, 255, 0) | `#00FF00` | Verde brillante - representación del héroe |
| Enemigo | (255, 0, 0) | `#FF0000` | Rojo intenso - amenaza peligrosa |
| Puerta | (0, 0, 255) | `#0000FF` | Azul estándar - paso entre salas |
| Objeto | (255, 255, 0) | `#FFFF00` | Amarillo dorado - items recolectables |
| Pared | (128, 128, 128) | `#808080` | Gris medio - estructura del dungeon |
| Decorado | (139, 69, 19) | `#8B4513` | Marrón tierra - elementos ambientales |
| Salida | (255, 215, 0) | `#FFD700` | Dorado brillante - objetivo final |
| Suelo | (0, 0, 0) | `#000000` | Negro absoluto - fondo del juego |

### Paleta Extendida (Fondos y UI)

| Elemento | RGB | Hex |
|----------|-----|-----|
| Fondo menú | (20, 20, 30) | `#14141E` |
| Borde UI | (60, 60, 80) | `#3C3C50` |
| TextoUI | (200, 200, 200) | `#C8C8C8` |
| HP baja | (255, 100, 100) | `#FF6464` |
| HP llena | (100, 255, 100) | `#64FF64` |
| Mana | (100, 100, 255) | `#6464FF` |

---

## 2. Especificaciones de Sprites

### Formato General
- **Extensión**: PNG
- **Profundidad**: 32-bit (RGBA)
- **Transparencia**: Sí (canal alpha)

### Dimensiones
- **Tile base**: 16x16 píxeles
- **Sprite individual**: 64x64 píxeles (para celdas de renderizado 4x4 del tile base)
- **Spritesheet**: Horizontal - múltiples frames en una sola fila

### Estructura de Spritesheets

```
[NOMBRE]_[ANIMACION]_XXXX.png

Ejemplo:
player_idle_0001.png  (frame 1)
player_idle_0002.png  (frame 2)
player_idle_0003.png  (frame 3)
player_idle_0004.png  (frame 4)
```

### Naming Convention
- Formato: `[entidad]_[estado]_[frame].png`
- Frames: 4 dígitos con padding (0001, 0002, etc.)

---

## 3. Sprites Necesarios

### 3.1 Jugador (Player)

| Animación | Frames | Descripción |
|-----------|--------|-------------|
| idle | 4 | Postura de espera, respiración |
| walk | 4 | Ciclo de caminata |
| attack | 3 | Golpe con arma |

**Ruta**: `data/sprites/player/`

**Colores característicos**:
- Cuerpo principal: `#00FF00` (verde)
- Borde/outline: `#004400` (verde oscuro)

---

### 3.2 Enemigos

| Tipo | Estados | Frames Total |
|------|---------|--------------|
| Esqueleton | idle(4), walk(4), attack(3), die(4) | 15 |
| Orco | idle(4), walk(4), attack(3), die(4) | 15 |
| Slime | idle(4), walk(4), attack(3), die(4) | 15 |
| Zombi | idle(4), walk(4), attack(3), die(4) | 15 |

**Ruta**: `data/sprites/enemies/`

**Colores característicos**:
- Cuerpo principal: `#FF0000` (rojo)
- Borde/outline: `#440000` (rojo oscuro)
- Variaciones: tintes adicionales para diferenciación

---

### 3.3 Items - Armas

| Tipo | Color Base | Notas |
|------|------------|-------|
| Puños | Gris claro `#AAAAAA` | Sin arma, ataques básicos |
| Espada | Plata `#C0C0C0` | Hoja plateada con芒果 |
| Hacha | Marrón `#8B4513` | Cabeza de metal gris |
| Martillo | Gris oscuro `#666666` | Mango marrón |

**Ruta**: `data/sprites/items/weapons/`

---

### 3.4 Items - Armaduras

| Tipo | Color Base | Descripción |
|------|------------|-------------|
| Ninguna | Verde jugador `#00FF00` | Sin protección |
| Ligera | Azul claro `#4169E1` | Cuero/simple |
| Media | Gris plateado `#A0A0A0` | Cota de malla |
| Pesada | Gris oscuro `#404040` | Armadura completa |

**Ruta**: `data/sprites/items/armor/`

---

### 3.5 Entornos

#### Paredes (4 tipos)
| ID | Nombre | Color RGB | Descripción |
|----|--------|-----------|-------------|
| wall_01 | Piedra normal | (100, 100, 100) | Piedras irregulares |
| wall_02 | Piedra oscura | (70, 70, 70) | Piedras con musgo |
| wall_03 | Ladrillo | (120, 80, 60) | Paredes de ladrillo |
| wall_04 | Piedra magical | (90, 90, 120) | Piedras con runas |

#### Suelo
| ID | Color RGB | Descripción |
|----|-----------|-------------|
| floor_01 | (20, 20, 20) | Suelo de piedra oscuro |
| floor_02 | (30, 25, 20) | Suelo de tierra |

#### Decorados
| ID | Color RGB | Descripción |
|----|-----------|-------------|
| rock | (80, 80, 80) | Roca suelta |
| pillar | (90, 90, 90) | Columna rota |
| torch | (255, 150, 50) | Antorcha encendida |
| chest | (139, 69, 19) | Cofre del tesoro |
| skeleton | (200, 200, 200) | Restos óseos |

**Ruta**: `data/sprites/environment/`

---

### 3.6 UI - Interfaz de Usuario

#### Menú Principal
| Elemento | Dimensiones | Color |
|----------|-------------|-------|
| Fondo | 800x600 | `#14141E` |
| Título | 400x80 | `#FFD700` (dorado) |
| Botón normal | 200x50 | `#3C3C50` |
| Botón hover | 200x50 | `#5C5C70` |
| Botón activo | 200x50 | `#2C2C40` |

#### HUD Elements
| Elemento | Dimensiones | Color |
|----------|-------------|-------|
| Barra HP | 200x20 | `#FF6464` (rojo) / `#64FF64` (verde) |
| Barra Mana | 200x20 | `#6464FF` |
| Icono arma | 32x32 | Variable según arma |
| Icono armadura | 32x32 | Variable según tipo |
| Marco inventario | 64x64 por ranura | `#3C3C50` |
| Indicador estado | 16x16 | Colores según estado |

**Ruta**: `data/sprites/ui/`

---

## 4. Estilo Visual

### Tema General
- **Temática**: Medieval gótico / DOOM-clásico
- **Atmósfera**: Oscura, amenazante, estratégica

### Principios de Diseño

1. **Visibilidad alta**: Colores primarios saturados para diferenciación rápida
2. **Contraste marcado**: Fondos oscuros con elementos brillantes
3. **Siluetas claras**: Formas reconocibles a pequeña escala
4. **Simplicidad funcional**: Sprites simples pero con distinción clara de estados

### Guía de Estilo

```
[TIPO] → [EJEMPLO VISUAL]

Jugador: Figura humanoide verde, silueta reconocible
         └─ Animaciones fluidas, frames de impacto claros

Enemigo: Silueta amenazante, ojos brillantes rojos
         └─ Animaciones de ataque amplias, muerte visible

Pared: Textura de piedra con sombras
       └─ Borde superior iluminado (fuente de luz superior)

Suelo: Gradiente sutil de claridad hacia el centro
       └─ Permite ver la posición del jugador

Items: Brillo dorado/amarillo sutil
       └─ Parpadeo leve para objetos importantes

Salida: Pulsación dorada
       └─ Efecto de luz que guía al jugador
```

### Animaciones - Tiempos Referencia

| Estado | Duración Frame | FPS |
|--------|----------------|-----|
| Idle | 200ms | 5 |
| Walk | 150ms | ~7 |
| Attack | 100ms | 10 |
| Die | 300ms | ~3 |

---

## 5. Estructura de Archivos

```
EscapeTheDungeonOfDoom/
├── data/
│   ├── sprites/
│   │   ├── player/
│   │   │   ├── player_idle_0001.png
│   │   │   ├── player_idle_0002.png
│   │   │   ├── player_idle_0003.png
│   │   │   ├── player_idle_0004.png
│   │   │   ├── player_walk_0001.png
│   │   │   ├── player_walk_0002.png
│   │   │   ├── player_walk_0003.png
│   │   │   ├── player_walk_0004.png
│   │   │   ├── player_attack_0001.png
│   │   │   ├── player_attack_0002.png
│   │   │   └── player_attack_0003.png
│   │   │
│   │   ├── enemies/
│   │   │   ├── skeleton/
│   │   │   ├── orc/
│   │   │   ├── slime/
│   │   │   └── zombie/
│   │   │
│   │   ├── items/
│   │   │   ├── weapons/
│   │   │   └── armor/
│   │   │
│   │   ├── environment/
│   │   │   ├── walls/
│   │   │   ├── floors/
│   │   │   └── props/
│   │   │
│   │   └── ui/
│   │       ├── menu/
│   │       └── hud/
│   │
│   └── audio/
│       ├── sfx/
│       └── music/
│
└── docs/
    └── GRAPHICS_SPECS.md
```

---

## 6. Checklist de Producción

### Fase 1: Assets Base
- [ ] Suelo básico (floor)
- [ ] Paredes (4 tipos)
- [ ] Jugador idle + walk + attack

### Fase 2: Enemigos
- [ ] Esqueleto (todos los estados)
- [ ] Orco (todos los estados)
- [ ] Slime (todos los estados)
- [ ] Zombi (todos los estados)

### Fase 3: Items y Entornos
- [ ] Armas (4 tipos)
- [ ] Armaduras (4 tipos)
- [ ] Decorados (rock, pillar, torch, chest)
- [ ] Salida

### Fase 4: UI
- [ ] Menú principal
- [ ] Botones
- [ ] HUD (barras, iconos)
- [ ] Pantallas de game over / victoria

---

## 7. Notas de Implementación

### Integración con Código
- Los sprites deben cargarse como texturas 2D
- Sistema de animación por índice de frame
- Colores base可以用来 filtrar elementos en debugging

### Optimización
- Spritesheet horizonta para reducir calls de render
- Usar atlas de texturas si el rendimiento lo requiere
- Pre-cargar sprites del área visible + adyacentes

### Testing Visual
- Verificar contraste en pantalla completa
- Probar con daltonismo (diferentes perfiles de color)
- Revisar legibilidad a diferentes escalas de zoom