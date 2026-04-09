# UX/UI Specification - Escape the Dungeon of Doom

## 1. Overview

Este documento define las especificaciones de interfaz y experiencia de usuario para "Escape the Dungeon of Doom". El objetivo es proporcionar una experiencia inmersiva estilo DOOM medieval con UI funcional y minimalista.

---

## 2. Visual Style

### 2.1 Estilo General

- **Temática**: Medieval/DOOM oscuro
- **Paleta de colores principal**:
  - Fondo menús: `#1a1a1a` (negro mate)
  - Texto primario: `#c9a227` (dorado antiguo)
  - Texto secundario: `#8b7355` (marrón cuero)
  - Highlight/selección: `#ff6b35` (naranja fuego)
  - Borde/acento: `#4a3728` (marrón oscuro)
  - Fondo HUD: `rgba(0, 0, 0, 0.7)` (negro semitransparente)

### 2.2 Tipografía

- **Fuente principal**: Usar fuente del sistema con fallback serif (Times New Roman, Georgia)
- **Tamaño título menú**: 48px
- **Tamaño opciones menú**: 28px
- **Tamaño HUD**: 18px
- **Tamaño texto informativo**: 16px

### 2.3 Sprites

- Formato: PNG
- Tamaño base: 64x64 píxeles
- Orientation: Horizontal spritesheet
- Ubicación: `data/sprites/`

---

## 3. Resolución y Display

### 3.1 Configuración Base

| Parámetro | Valor |
|-----------|-------|
| Resolución por defecto | 800x600 |
| Relación aspecto | 4:3 |
| Modo ventana | Ventana con bordes |
| Soporte fullscreen | Sí |

### 3.2 Fullscreen

- Toggle en menú de opciones
- Cambia entre modo ventana (800x600) y pantalla completa
- Mantiene relación de aspecto con letterboxing si es necesario
- Persistir opción en `config/options.json`

---

## 4. Menú Principal (Main Menu)

### 4.1 Estructura

```
+----------------------------------+
|                                  |
|      ESCAPE THE DUNGEON          |
|        OF DOOM                  |
|                                  |
|        [ START GAME ]            |
|                                  |
|        [  OPTIONS  ]            |
|                                  |
|        [   EXIT    ]            |
|                                  |
+----------------------------------+
```

### 4.2 Posicionamiento

- **Contenedor**: Centrado horizontal y verticalmente
- **Espaciado entre opciones**: 40px
- **Margen inferior del título**: 60px
- **Título**: Texto en dorado `#c9a227`, 48px, centrado
- **Opciones**: Texto en dorado `#c9a227`, 28px
- **Hover**: Texto cambia a naranja `#ff6b35`, efecto de escala 1.05x

### 4.3 Comportamiento

- Navegación con ↑↓ (flechas) y Enter para seleccionar
- Click del mouse también funcional
- Sonido de "hover" opcional (click al seleccionar)
- Fondo: Pantalla negra o imagen de fondo difusa del dungeon

### 4.4 Transiciones

- Al seleccionar "Start Game": Transición a LevelTransition (Level 1)
- Al seleccionar "Options": Ir a menú de opciones
- Al seleccionar "Exit": Cerrar aplicación

---

## 5. Menú de Pausa (Pause Menu)

### 5.1 Activación

- Se abre al presionar **ESC** durante el juego
- El juego se pausa completamente (movimiento, IA, temporizadores)
- Música de fondo se pausa

### 5.2 Estructura

```
+----------------------------------+
|                                  |
|           PAUSED                |
|                                  |
|        [  RESUME  ]             |
|                                  |
|        [  OPTIONS  ]            |
|                                  |
|     [ EXIT TO MENU ]           |
|                                  |
+----------------------------------+
```

### 5.3 Posicionamiento

- Mismo estilo que menú principal
- "PAUSED" como título centrado
- Fondo: Oscurecer juego subyacente (overlay negro 50% opacidad)

### 5.4 Comportamiento

- **RESUME**: Cerrar menú y continuar juego
- **OPTIONS**: Ir a menú de opciones
- **EXIT TO MENU**: Volver al menú principal (reiniciar juego completo)
- Navegación con ↑↓ y Enter
- ESC también cierra el menú (alternativa a Resume)

---

## 6. Menú de Opciones (Options Menu)

### 6.1 Estructura

```
+----------------------------------+
|                                  |
|          OPTIONS                |
|                                  |
|  FULLSCREEN:        [ OFF ]     |
|                                  |
|  TURN SPEED:    [====●===] 90°/s
|       (60°/s ----------- 120°/s)
|                                  |
|       [ BACK TO MENU ]          |
|                                  |
+----------------------------------+
```

### 6.2 Opciones

| Opción | Tipo | Valores | Default |
|--------|------|---------|---------|
| Fullscreen | Toggle | ON / OFF | OFF |
| Turn Speed | Slider | 60 - 120 °/s | 90 °/s |

### 6.3 Controles de Slider

- Teclas ←→ para ajustar valor (step: 10 °/s)
- Click y arrastrar en el slider
- Click en slider para mover directamente
- Valor mostrado en tiempo real

### 6.4 Persistencia

- Guardar en `config/options.json` al cambiar
- Cargar al iniciar juego
- Aplicar cambios inmediatamente (fullscreen)

### 6.5 Navegación

- BACK TO MENU: Volver al menú anterior (principal o pausa)
- Tecla ESC también vuelve al menú anterior

---

## 7. HUD (Heads-Up Display)

### 7.1 Posicionamiento

- **Ubicación**: Esquina inferior izquierda
- **Margen**: 20px desde bordes
- **Layout horizontal**: [ICONO ARMA] [NOMBRE ARMA] | [ICONO ARMADURA] [NOMBRE ARMADURA]

### 7.2 Elementos

```
+--------------------------------------------------+
|                                                  |
|                                                  |
|  [⚔️ Espada] | [🛡️ Media]              (LEVEL 3)
|                                                  |
+--------------------------------------------------+
```

### 7.3 Vida del Jugador

| Estado | Comportamiento |
|--------|----------------|
| Normal (oculta) | No mostrar barra de vida |
| Presionando TAB | Mostrar barra de vida por 2 segundos |
| Release TAB | Ocultar gradualmente (fade 0.3s) |

### 7.4 Visualización de Vida

- **Barra de vida**: Fondo oscuro `#2a2a2a`, relleno rojo `#cc3333`
- **Tamaño**: 200px x 20px
- **Posición HUD temporal**: Sobre el equipamiento cuando TAB está activo
- **Formato texto**: "HP: 100/100" (opcional, debajo de la barra)
- **Porcentaje**: Mostrar daño recibido visualmente

### 7.5 Equipamiento

- **Icono**: Sprite 32x32 del objeto
- **Nombre**: Texto 18px
- **Cuando sin equipo**: Mostrar "Desarmado" / "Sin armadura"
- **Actualización**: Inmediata al equipar nuevo item

### 7.6 Nivel Actual

- **Ubicación**: Esquina superior derecha
- **Margen**: 20px
- **Formato**: "LEVEL 3" (número en romano opcional)
- **Estilo**: Texto dorado `#c9a227`, 24px

### 7.7 Elementos NO incluidos

- **SIN MINIMAPA**: Por diseño, para mantener tensión y exploración

---

## 8. Pantallas de Estado (State Scenes)

### 8.1 GameOverScene

| Aspecto | Detalle |
|---------|---------|
| Activación | Cuando vida del jugador llega a 0 |
| Duración | 2 segundos |
| Fondo | Negro `#000000` |
| Texto | "YOU DIED" en rojo `#cc3333`, 64px, centrado |
| Transición | Automática a menú principal |

```
+----------------------------------+
|                                  |
|                                  |
|           YOU DIED              |
|                                  |
|                                  |
+----------------------------------+
```

### 8.2 VictoryScene

| Aspecto | Detalle |
|---------|---------|
| Activación | Completar nivel 5 (último nivel) |
| Duración | 5 segundos |
| Fondo | Negro `#000000` |
| Texto | "VICTORY!" en dorado `#c9a227`, 64px, centrado |
| Subtexto | "You escaped the Dungeon of Doom!" |
| Transición | Automática a menú principal |

```
+----------------------------------+
|                                  |
|                                  |
|          VICTORY!               |
|                                  |
|  You escaped the Dungeon       |
|         of Doom!               |
|                                  |
+----------------------------------+
```

### 8.3 LevelTransitionScene

| Aspecto | Detalle |
|---------|---------|
| Activación | Al iniciar cada nivel |
| Fase 1 | Pantalla negra 2 segundos |
| Fase 2 | Nombre del nivel 2 segundos |
| Fondo | Negro `#000000` |
| Texto nivel | Nombre en dorado `#c9a227`, 48px, centrado |

### 8.4 Nombres de Niveles

| Nivel | Nombre a mostrar |
|-------|------------------|
| 1 | DUNGEON |
| 2 | CASTLE |
| 3 | CAMP |
| 4 | FOREST |
| 5 | MOUNTAIN PASS |

---

## 9. Controles (Controls)

### 9.1 Tabla de Controles

| Tecla | Acción | Contexto |
|-------|--------|----------|
| W | Moverse adelante | Juego |
| A | Moverse izquierda | Juego |
| S | Moverse atrás | Juego |
| D | Moverse derecha | Juego |
| ← (Left) | Girar vista izquierda | Juego |
| → (Right) | Girar vista derecha | Juego |
| Espacio | Atacar | Juego |
| E | Interactuar (recoger/abrir) | Juego |
| TAB | Mostrar vida temporalmente | Juego |
| ESC | Abrir menú de pausa | Juego |
| F3 | Toggle debug overlay | Juego |

### 9.2 Velocidad de Giro

- **Rango**: 60°/s a 120°/s
- **Default**: 90°/s
- **Control**: Opción en menú de opciones
- **Variable**: `TURN_SPEED` en configuración

### 9.3 Visualización de Controles

- No mostrar controles en pantalla durante el juego (minimalista)
- Pantalla de "How to Play" opcional al inicio (botón en menú principal)

---

## 10. Debug Overlay (F3)

### 10.1 Activación

- Toggle con **F3** durante el juego
- Muestra información de debug superpuesta

### 10.2 Contenido

```
FPS: 60
Player: (x, y)
Angle: 90°
Weapon: Espada (25%)
Armor: Media (50%)
Enemies: 3/5
```

### 10.3 Posición

- Esquina superior izquierda
- Fondo semitransparente para legibilidad
- Texto pequeño (14px)

---

## 11. Architecture de UI

### 11.1 Clases Principales

```
src/
  ui/
    menu.py           # MenuScene, PauseMenu
    options.py        # OptionsScene
    hud.py            # HUD class
    screens/
      game_over.py    # GameOverScene
      victory.py      # VictoryScene
      transition.py   # LevelTransitionScene
    components/
      button.py       # Botón reutilizable
      slider.py       # Slider para opciones
      text.py         # Texto estilizado
    renderer.py       # Renderizado de UI
```

### 11.2 Scene Manager

- Sistema de escenas para transiciones
- Estados: MENU, GAME, PAUSED, OPTIONS, GAMEOVER, VICTORY, TRANSITION
- Pila de escenas para menús sobre juego

### 11.3 Eventos de UI

| Evento | Descripción |
|--------|-------------|
| UI_OPEN_MENU | Abre menú principal |
| UI_OPEN_PAUSE | Abre menú de pausa |
| UI_CLOSE_MENU | Cierra menú actual |
| UI_OPEN_OPTIONS | Abre menú de opciones |
| UI_SHOW_HEALTH | Muestra vida (TAB) |
| UI_HIDE_HEALTH | Oculta vida |

---

## 12. Constantes para constants.py

```python
# ==================== UI ====================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Escape the Dungeon of Doom"

# Colores UI
UI_COLOR_BACKGROUND = (26, 26, 26)        # #1a1a1a
UI_COLOR_TEXT_PRIMARY = (201, 162, 39)     # #c9a227
UI_COLOR_TEXT_SECONDARY = (139, 115, 85)  # #8b7355
UI_COLOR_HIGHLIGHT = (255, 107, 53)        # #ff6b35
UI_COLOR_BORDER = (74, 55, 40)             # #4a3728
UI_COLOR_HEALTH = (204, 51, 51)            # #cc3333
UI_COLOR_HEALTH_BG = (42, 42, 42)          # #2a2a2a

# Fuentes
UI_FONT_TITLE = 48
UI_FONT_MENU = 28
UI_FONT_HUD = 18
UI_FONT_DEBUG = 14

# HUD
HUD_MARGIN = 20
HUD_HEALTH_BAR_WIDTH = 200
HUD_HEALTH_BAR_HEIGHT = 20
HUD_TAB_DISPLAY_TIME = 2.0  # segundos
HUD_TAB_FADE_TIME = 0.3     # segundos

# Turn Speed
TURN_SPEED_MIN = 60   # grados/segundo
TURN_SPEED_MAX = 120
TURN_SPEED_DEFAULT = 90
TURN_SPEED_STEP = 10

# Tiempos de transición
TRANSITION_BLACK_TIME = 2.0    # segundos
TRANSITION_NAME_TIME = 2.0     # segundos
GAMEOVER_DISPLAY_TIME = 2.0    # segundos
VICTORY_DISPLAY_TIME = 5.0     # segundos

# Niveles
LEVEL_NAMES = {
    1: "DUNGEON",
    2: "CASTLE",
    3: "CAMP",
    4: "FOREST",
    5: "MOUNTAIN PASS",
}
```

---

## 13. Archivo de Opciones (options.json)

```json
{
    "fullscreen": false,
    "turn_speed": 90,
    "volume_music": 0.7,
    "volume_sfx": 0.8
}
```

---

## 14. Flujo de Estados

```
MENU ──[Start Game]──> TRANSITION ──[Level 1]──> GAME
                                                      │
                                                      ├──[ESC]──> PAUSE
                                                      │              │
                                                      │              ├──[Resume]──> GAME
                                                      │              │
                                                      │              ├──[Options]──> OPTIONS ──[Back]──> PAUSE
                                                      │              │
                                                      │              └──[Exit to Menu]──> MENU
                                                      │
                                                      ├──[Die]──> GAMEOVER ──[2s]──> MENU
                                                      │
                                                      ├──[Complete L5]──> VICTORY ──[5s]──> MENU
                                                      │
                                                      └──[Exit L1-4]──> TRANSITION ──> GAME
```

---

## 15. Notas de Implementación

### 15.1 Rendering

- UI renderizada después del mundo del juego (sobre capa)
- Usar surfaces de pygame para elementos de UI
- Support para redimensionar si se implementa fullscreen

### 15.2 Input

- Gestionar input de UI separado del input de juego
- Prevenir "input bleeding" entre UI y juego
- Tab debe funcionar incluso en menú de pausa

### 15.3 Audio

- Sonido de hover en menús (opcional)
- Sonido de click al seleccionar
- Música de menú y música de juego separadas
- Pausar música al pausar juego

### 15.4 Accesibilidad

- Nombres de items legibles
- Contraste suficiente entre texto y fondo
- Tamaño de hitboxes de botones adecuado (mínimo 40px altura)
