# AGENTS.md - Escape the Dungeon of Doom

## 1. Descripción del Proyecto

Videojuego de acción en primera persona estilo DOOM medieval. El jugador debe escapar de 5 niveles de mazmorras/escenarios, con mecánicas de sigilo y combate cuerpo a cuerpo.

### 1.1 Funcionalidad Principal
- 5 mapas/niveles progression secuencial:
  1. **Dungeon** (mazmorra subterránea)
  2. **Castle** (planta baja castillo)
  3. **Camp** (campamento alrededor del castillo)
  4. **Forest** (bosque amplio)
  5. **Mountain Pass** (paso de montaña)
- Sistema de muerte: Game over completo (2 segundos) + reinicio del juego
- Movimiento en 4 direcciones, mirada con rotación horizontal del sprite
- Enemigos con patrullas predefinidas (mismo recorrido cada juego)
- Punto de entrada y salida por nivel (llegar a la salida para avanzar)
- Puertas interactuables (abrir/cerrar con input cuando está en proximidad)
- Decorados con colisión y diferentes sprites según tipo
- Sin límite de tiempo por nivel (infinito inicialmente)
- Sin sistema de guardado/progreso (siempre comienza desde el principio)
- La salida es una puerta más grande (2 celdas vs 1 celda) con sprite especial
- Objetos tirados permanecen en el suelo (máximo 1 por celda)
- Al completar 5 niveles: pantalla de victoria, reinicio tras 5 segundos
- Mapa de test: sala con todas las armas/armaduras, otra sala con enemigo configurable
- Objetos al cambiar de nivel desaparecen
- Transiciones entre niveles (pantalla negra, 2 segundos)
- Nombre del nivel shown during 2 seconds al entrar

### 1.2 Sistema de Combate
- Armas cuerpo a cuerpo: puños, espada, hacha, martillo (cada una con velocidad y daño diferentes)
- Armaduras: ninguna, ligera, media, pesada (afectan velocidad y defensa)
- Daño: `daño = daño_arma × penetrabilidad_armadura` (porcentual)
- Backstab: 25% más daño al atacar por detrás
- Animación de ataque con ventana de esquiva (0.3 segundos)
- Una sola arma y armadura equipadas (equipado directo, tirar anterior)
- Todos tienen 100% vida, sin curaciones
- Ataque con barra espaciadora
- Inventario vacío no visible, jugador deduce del arma en pantalla
- Sonido de ataque opcional (generado procedural si no hay MP3)

### 1.3 Sistema de Enemigos
- Estados: solo patrol, chase, attack
- Patrullas: coordenadas definidas (circular o ida-y-vuelta), sin puntos de espera
- Velocidad fija (misma para todos los enemigos): 2 celdas/segundo
- Chase: seguimiento directo (no pathfinding)
- Deteección basada solo en distancia (no ruido)
- Radio de detección: mayor en niveles 1-2, menor en niveles 3-4, mayor que nivel 1 en nivel 5
- Campo de visión: 120°
- Distancia de ataque: 1 celda
- Los enemigos pueden abrir puertas
- Puertas bloquean visión
- Las paredes bloquean el ataque del enemigo
- Cooldown de ataque: 1 segundo
- Al colisionar con el jugador: ataca inmediatamente
- Con animación de ataque
- Configurables (arma + armadura), combinaciones varían en dificultad
- Todos son humanos
- Animaciones: caminar, attack, morir
- Enemigos desaparecen al morir
- Un solo nivel de dificultad para todos los enemigos
- Las paredes bloquean la línea de visión del jugador

### 1.4 Sistema de Objetos
- 2 armas + 2 armaduras por nivel (primeros 3 niveles)
- Armadura/arma más pesada disponible en nivel 2
- Equipar directo, objeto anterior se tira al suelo
- Persisten en el nivel, se mantiene al cambiar de nivel (equipo solo)
- Niveles 4-5: solo supervivencia (sin objetos)
- Al completar juego, se reinicia todo
- Máximo 1 objeto por celda

### 1.5 UI/HUD
- Menú principal: Start, Opciones, Salir
- Menú pausado: Resume, Opciones, Salir
- Opciones: Pantalla completa/ventana, velocidad de giro (60-120°/s)
- Pausa con ESC
- Health bar oculta por defecto
- Pulsar TAB para ver vida actual (borde superior izquierdo)
- Resumen de controles en pantalla de carga (3 segundos)
- Nombre del nivel al entrar (2 segundos)
- Sin minimapa
- Exploración y memoria para encontrar la salida
- Sin peligros ambientales (pozos, trampas)

### 1.6 Tecnologías
- **Lenguaje**: Python
- **Framework**: Pygame
- **Gestión**: UV
- **Control de versiones**: Git
- **Formato de sprites**: PNG
- **Formato de audio**: MP3 (o procedural si no hay)
- **Resolución**: Modificable (por defecto 800x600)
- **Tile size**: Configurable (para 800x600 con mapa 48x48)

### 1.7 Limitaciones
- Sin sistema de niveles o habilidades
- Sin curación
- Sin guardado/progreso
- Primera persona (no top-down)
- Gráficos: sprites PNG o cuadrados de color sólido por defecto
- Sonidos: opcionales inicialmente
- Sin historia/narrativa
- El jugador no puede agacharse

---

## 2. Reglas de Calidad

| Principio | Aplicación |
|-----------|------------|
| **SOLID** | Diseño orientado a componentes, dependencias mínimas |
| **DRY** | Extraer lógica compartida a funciones/base classes |
| **YAGNI** | Implementar solo lo necesario para el requisito actual |
| **SRP** | Una responsabilidad por clase/módulo |
| **Nombres claros** | Descriptivos, en inglés ( snake_case ) |
| **Comentarios** | Una línea por función/método (docstring) |

---

## 3. Controles

| Tecla | Acción |
|-------|--------|
| WASD | Moverse por el mapa |
| ← → (flechas) | Girar vista horizontal |
| Espacio | Atacar |
| E | Recoger objeto / Abrir puerta |
| I | Tirar arma actual |
| J | Tirar armadura actual |
| TAB | Mostrar vida |
| ESC | Pausar / Menú |

---

## 4. Estructura del Proyecto

### 4.1 Arquitectura
Orientada a componentes. Ficheros externos JSON para configuración:

```
/data
  /maps/          # Mapas en CSV ( _, #, letras/números)
  /patrols/       # Rutas de patrulla (JSON)
  /enemies/       # Configuración de enemigos (JSON)
  /items/         # Armas y armaduras (JSON)
  /sprites/       # Imágenes PNG (pixel art)
  /audio/         # Sonidos MP3

/src
  /core/          # Motor del juego
  /components/    # Componentes reutilizables
  /entities/      # Entidades (jugador, enemigos)
  /systems/       # Sistemas (combate, IA, input)
  /utils/         # Utilidades

/config           # Configuración general (config.json)
```

### 4.2 Formato de Mapas (CSV)
Caracteres:
- `_` = vacío (suelo transitable)
- `#` = pared (bloquea movimiento)
- `P` = punto de entrada (Player spawn)
- `E` = salida (Exit, 2 celdas)
- `D` = puerta (Door)
- `0-9` = enemigo (referencia a configuración)
- `a-z` = objeto (arma/armadura)
- `.` = decorado (sin función, con colisión)

Ejemplo (8x6):
```
########
#P_____#
#__##_D#
#__a1__#
#_..2__E
########
```

### 4.3 Sprites y Animaciones
- Formato PNG spritesheet horizontal
- Mapping en JSON (carácter → sprite)
- Por defecto: cuadrado de color sólido si no hay imagen
- 5 frames por animación (1 segundo)
- Dimensiones sprites: configurables (sugerido 64x64 px)
- Animaciones: caminar, attack, morir
- Decorados tienen sprites diferenciados (4-5 tipos)
- Vista 2D con sprites frontales (estilo DOOM clásico)

### 4.4 Colores por Defecto
| Entidad | Color (RGB) |
|---------|-------------|
| Jugador | Verde (0, 255, 0) |
| Enemigo | Rojo (255, 0, 0) |
| Puerta | Azul (0, 0, 255) |
| Objeto | Amarillo (255, 255, 0) |
| Pared | Gris (128, 128, 128) |
| Decorado | Marrón (139, 69, 19) |
| Salida | Dorado (255, 215, 0) |

---

## 5. Comandos

```bash
# Desarrollar
uv run python -m src.main        # Ejecutar juego
uv run pytest                    # Tests
uv run pylint src/               # Linting

# Generar contenido
python tools/generate_map.py     # Generador de mapas
```

---

## 6. Preguntas Clarificadoras

### Respondidas
1. Vista: Primera persona ✓
2. Mirada horizontal: Rotación del sprite ✓
3. Niveles: Secuenciales ✓
4. Límite de tiempo: Infinito inicialmente ✓
5. Formato sprites: PNG ✓
6. Patrulles sin puntos de espera ✓
7. Puertas: Input del jugador en proximidad ✓
8. Guardado: No, siempre desde el principio ✓
9. Resolución: Modificable (800x600 por defecto) ✓
10. Ataque: Tecla dedicada (barra espaciadora) ✓
11. Condición de victoria: Llegar a la salida vivo ✓
12. Enemigos: Muchos, pasable controlando tiempos ✓
13. UI: Health bar oculta, TAB para ver ✓
14. Framerate: 60 FPS ✓
15. Salida: Puerta grande (2 celdas), sprite especial ✓
16. Objetos: Siempre visibles ✓
17. Movimiento: WASD + flechas para vista ✓
18. Tile size: Configurable ✓
19. Equipar: Directo, tirar anterior con I/J ✓
20. Muerte: Game over 2s + reinicio juego ✓
21. Puertas estado: Variable (abiertas/cerradas) ✓
22. Decorados: Con colisión, sprites diferenciados ✓
23. Sonidos: MP3/opcional, procedural si no hay ✓
24. Controles: WASD/espacio/E/I/J/TAB/flechas/ESC ✓
25. Fin del juego: Pantalla victoria 5s + reinicio ✓
26. Objetos tirados: Permanecen en el suelo ✓
27. Objetos por nivel: 2 armas + 2 armaduras (niveles 1-3) ✓
28. Detección: Radio variable por nivel ✓
29. Puertas bloquean visión: Sí, enemigos pueden abrir ✓
30. Tutorial: Resumen en carga 3s ✓
31. Nombre: Escape the Dungeon of Doom ✓
32. Menú: Start, Opciones, Salir ✓
33. Menú pausa: Resume, Opciones, Salir ✓
34. Opciones: Fullscreen, velocidad giro (60-120°/s) ✓
35. Vista: 2D con sprites frontales (estilo DOOM) ✓
36. Progreso entre niveles: Equipo + vida, posición reinicia ✓
37. CSV mapa: Formato con ejemplo definido ✓
38. Estados enemigo: Patrol, chase, attack ✓
39. Daño: Daño arma × Penetrabilidad armadura ✓
40. Mapa test: Sala con todos los items + sala con enemigo configurable ✓
41. Frames animación: 5 frames por animación (1 segundo) ✓
42. Spritesheet: Formato horizontal ✓
43. Niveles 4-5: Supervivencia sin objetos ✓
44. Indicador dirección: No ✓
45. Tamaño mapa: 48x48 ✓
46. Velocidad giro: 60-120°/s ✓
47. Pausa: ESC con menú resume ✓
48. Inventario vacío: No visible ✓
49. Muerte mensaje: Game over 2s ✓
50. Decorados: 4-5 tipos ✓
51. Objetos al cambiar nivel: Desaparecen ✓
52. Objetos disponibles: Al inicio del nivel ✓
53. Distancia interacción: 2 celdas ✓
54. Campo visión enemigo: 120° ✓
55. Equipar con inventario lleno: Equipar directo, tirar anterior ✓
56. Armadura sprite: No afecta sprite ✓
57. Decorados sprites específicos: Sí ✓
58. Objetos límite: 1 por celda ✓
59. Velocidad armadura: 1.0/0.8/0.6/0.3 ✓
60. Velocidad ataque: 1.0/0.9/0.7/0.5 ✓
61. Daño armas: 10%/25%/40%/70% ✓
62. Penetrabilidad armadura: 1.0/0.75/0.5/0.25 ✓
63. Velocidad movimiento: 3 celdas/segundo ✓
64. Colores por defecto: Verde/Rojo/Azul/Amarillo/Gris/Marrón/Dorado ✓
65. Sprite loading: Mapping en JSON ✓
66. Niveles nombres: Dungeon, Castle, Camp, Forest, Mountain Pass ✓
67. Ruido/footsteps: No, solo distancia ✓
68. Animación ataque: 0.3 segundos ✓
69. Transiciones: Pantalla negra 2 segundos ✓
70. Historia/narrativa: No ✓
71. Puertas sprite especial: Sí ✓
72. Transición duración: 2 segundos ✓
73. Velocidad enemigos: Fija (2 celdas/segundo) ✓
74. Input durante transición: Se ignora ✓
75. Decorados colisión: Sí (todos) ✓
76. Chase comportamiento: Seguimiento directo ✓
77. Nombre nivel: Se muestra 2 segundos ✓
78. HUD adicional: No ✓
79. Indicador objetos: No visible ✓
80. Vida cero: Game over + reinicio ✓
81. Salir durante partida: Sí con ESC ✓
82. Peligros ambientales: No ✓
83. Enemigos al morir: Desaparecen ✓
84. Cooldown ataque enemigo: 1 segundo ✓
85. Colisión jugador-enemigo: Ataque inmediato ✓
86. Dificultad enemigos: 1 nivel (todos iguales) ✓
87. Sprites por defecto: Cuadrados de color sólido ✓
88. Sonido ataque: Sí (procedural si no hay MP3) ✓
89. Paredes bloquean ataque enemigo: Sí ✓
90. Distancia ataque enemigo: 1 celda ✓
91. Paredes bloquean visión jugador: Sí ✓
92. Backstab: Sí (+25% daño) ✓
93. Agacharse: No ✓
94. Sonido por defecto: Procedural ✓
95. Ataque enemigo: Con animación ✓
96. Config general: config.json ✓
97. Tile size para 800x600 y 48x48: ~16-20 px (calculado) ✓
98. Sprites dimensiones: Configurables ✓

### Nuevas Preguntas (1-20, responde con tu opción)

1. **¿Qué tamaño de tile recomiendas para 800x600 con mapa 48x48?**
   - [ ] 12 píxeles
   - [X] 16 píxeles
   - [ ] 20 píxeles
   - [ ] Tu respuesta: _____________

2. **¿Necesitas archivo de configuración general (config.json)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

3. **¿Dimensiones de sprites (ancho x alto)?**
   - [ ] 32x32
   - [X] 64x64
   - [ ] 128x128
   - [ ] Tu respuesta: _____________

4. **¿Requisitos de memoria/rendimiento?**
   - [X] Estándar (sin requisitos especiales)
   - [ ] Alto rendimiento necesario
   - [ ] Tu respuesta: _____________

5. **¿Sistema de logging para debugging?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: ¿Qué nivel? _____________

6. **¿Tests desde el inicio?**
   - [X] Sí, desde el inicio
   - [ ] Se pueden añadir después
   - [ ] Tu respuesta: _____________

7. **¿Qué nivel de logging?**
   - [ ] DEBUG
   - [X] INFO
   - [ ] WARNING
   - [ ] Tu respuesta: _____________

8. **¿Formato de log?**
   - [ ] Solo console
   - [X] Console + archivo
   - [ ] Tu respuesta: _____________

9. **¿Frameworks de test?**
   - [ ] pytest (Recomendado)
   - [ ] unittest
   - [X] pytest
   - [ ] Tu respuesta: _____________

10. **¿Cubrimiento de tests esperado inicial?**
    - [ ] 100%
    - [X] Core logic (50-70%)
    - [ ] Mínimo
    - [ ] Tu respuesta: _____________

11. **¿Necesitas inicializar UV/dependencias?**
    - [X] Sí, con uv init
    - [ ] No
    - [ ] Tu respuesta: _____________

12. **¿Archivo pyproject.toml?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

13. **¿Requisitos de dependencies en pyproject.toml?**
    - [X] pygame
    - [ ] pygame, numpy
    - [ ] Tu respuesta: _____________

14. **¿Archivos de datos (mapas JSON) se crean manualmente o con script?**
    - [ ] Manualmente
    - [ ] Script generador
    - [X] Ambos
    - [ ] Tu respuesta: _____________

15. **¿El script generador está en /tools?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

16. **¿Cómo se validan los mapas CSV?**
    - [X] Por código (al cargar)
    - [ ] No se validan
    - [ ] Tu respuesta: _____________

17. **¿Hay algún formato específico para los JSON de configuración?**
   - [X] Estándar JSON
   - [ ] JSON con comentarios
   - [ ] Tu respuesta: _____________

18. **¿Los JSON usan formato con comentarios (JSONC)?**
    - [ ] No, estándar JSON
    - [X] Sí
    - [ ] Tu respuesta: _____________

19. **¿Orden de carga de archivos al iniciar el juego?**
    - [X] config → sprites → maps → enemies → items
    - [ ] Libre
    - [ ] Tu respuesta: _____________

20. **¿Manejo de errores al cargar archivos?**
    - [X] Logging + continuar condefaults
    - [ ] Fatal error
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (21-40, responde con tu opción)

21. **¿pantalla de carga muestra progreso?**
    - [ ] No, simplemente muestra el resumen
    - [X] Sí, barra de progreso
    - [ ] Tu respuesta: _____________

22. **¿La barra de progreso muestra porcentaje?**
    - [ ] Sí
    - [ ] No
    - [X] Tu respuesta: No hay barra de progreso.

23. **¿Tiempo de carga estimado por nivel?**
    - [ ] < 1 segundo
    - [X] 1-2 segundos
    - [ ] > 2 segundos
    - [ ] Tu respuesta: _____________

24. **¿El juego tiene modo debug/cheats?**
    - [ ] No
    - [X] Sí (para testing)
    - [ ] Tu respuesta: _____________

25. **¿Los mapas tienen límite de enemigos?**
    - [X] No, pero recomendado < 20 por rendimiento
    - [ ] Sí, máximo definido
    - [ ] Tu respuesta: _____________

26. **¿Los decorados tienen sprites animados?**
    - [ ] No
    - [X] Solo algunos (antorchas)
    - [ ] Todos
    - [ ] Tu respuesta: _____________

27. **¿Las antorchas parpadean?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

28. **¿Sistema de partículas (polvo, sangre)?**
    - [ ] No
    - [X] Solo sangre al morir
    - [ ] Ambos
    - [ ] Tu respuesta: _____________

29. **¿Efectos de sonido procedimentales usan librería específica?**
    - [X] pygame.mixer o simple synthesis
    - [ ] soundfile
    - [ ] Tu respuesta: _____________

30. **¿Música de fondo (BGM)?**
    - [ ] No
    - [X] Opcional (loop)
    - [ ] Tu respuesta: _____________

31. **¿La BGM se cambia por nivel?**
    - [ ] No
    - [X] Sí (tema diferente por nivel)
    - [ ] Tu respuesta: _____________

32. **¿Volumen configurable?**
    - [X] Sí (en opciones)
    - [ ] No
    - [ ] Tu respuesta: _____________

33. **¿Guarda la configuración entre sesiones?**
    - [ ] No
    - [X] Sí (opciones solo)
    - [ ] Tu respuesta: _____________

34. **¿Formato de guardado de opciones?**
    - [X] JSON
    - [ ] txt
    - [ ] Tu respuesta: _____________

35. **¿Ubicación del archivo de opciones?**
    - [X] Directorio del juego
    - [ ] AppData/AppConfig
    - [ ] Tu respuesta: _____________

36. **¿El juego detecta si hay archivos de datos faltantes?**
    - [X] Sí, con warning
    - [ ] No
    - [ ] Tu respuesta: _____________

37. **¿Continúa el juego si faltan sprites?**
    - [X] Sí (usa colores por defecto)
    - [ ] No
    - [ ] Tu respuesta: _____________

38. **¿El juego detecta la resolución de pantalla del sistema?**
    - [ ] No
    - [X] Sí, para defaults
    - [ ] Tu respuesta: _____________

39. **¿Permite resolución custom más allá de las opciones?**
    - [ ] No
    - [X] Sí (edición manual de config)
    - [ ] Tu respuesta: _____________

40. **¿El juego soporta keyboard input multilingüe?**
    - [X] Solo inglés
    - [ ] UTF-8 completo
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (41-60, responde con tu opción)

41. **¿El juego usa virtual keyboard en móvil?**
    - [X] No (escritorio only)
    - [ ] Sí
    - [ ] Tu respuesta: _____________

42. **¿El juego funciona en Linux/Mac/Windows?**
    - [X] Todos
    - [ ] Solo Windows
    - [ ] Tu respuesta: _____________

43. **¿El código usa type hints?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

44. **¿El código usa type hints completos o parcial?**
    - [ ] Completos
    - [X] Parciales (principales funciones)
    - [ ] Tu respuesta: _____________

45. **¿Hay documento de arquitectura además de AGENTS.md?**
    - [ ] No
    - [X] No por ahora
    - [ ] Tu respuesta: _____________

46. **¿El código usa dataclasses o clases normales?**
    - [ ] Clases normales
    - [X] dataclasses donde sea apropiado
    - [ ] Tu respuesta: _____________

47. **¿Patrón de diseño usado (MVC, ECS, otro)?**
    - [X] Componentes (ECS-like)
    - [ ] MVC
    - [ ] Tu respuesta: _____________

48. **¿Cómo se manejan las entidades (clase base)?**
    - [X] Entidad base + componentes
    - [ ] Herencia simple
    - [ ] Tu respuesta: _____________

49. **¿El game loop está en clase dedicada?**
    - [X] Sí (Game class)
    - [ ] No (funciones sueltas)
    - [ ] Tu respuesta: _____________

50. **¿Hay sistema de eventos para comunicación entre sistemas?**
    - [X] Sí (patrón observer/bus)
    - [ ] No (coupling directo)
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (61-80, responde con tu opción)

51. **¿Sistema de eventos es síncrono o asíncrono?**
    - [X] Síncrono
    - [ ] Asíncrono
    - [ ] Tu respuesta: _____________

52. **¿Los sistemas (input, physics, render) se actualizan en orden fijo?**
    - [X] Sí (input → physics → render)
    - [ ] No
    - [ ] Tu respuesta: _____________

53. **¿El renderer usa double buffering?**
    - [X] Sí (pygame default)
    - [ ] No
    - [ ] Tu respuesta: _____________

54. **¿Se redibuja toda la pantalla cada frame?**
    - [X] Sí
    - [ ] No (dirty rects)
    - [ ] Tu respuesta: _____________

55. **¿Los sprites se cargan en memoria una sola vez?**
    - [X] Sí (cache)
    - [ ] Cada frame
    - [ ] Tu respuesta: _____________

56. **¿El juego usavsync?**
    - [X] Sí (60 FPS capped)
    - [ ] No
    - [ ] Tu respuesta: _____________

57. **¿Qué pasa si el framerate baja mucho (< 30)?**
    - [ ] Se reduce velocidad del juego proporcionalmente
    - [X] Se mantiene velocidad fixed, se saltan los frames.
    - [ ] Tu respuesta: _____________

58. **¿Sistema de collisiones usa AABB o circle?**
    - [X] AABB (cuadrados)
    - [ ] Circle
    - [ ] Tu respuesta: _____________

59. **¿Las colisiones se resuelven inmediatamente?**
    - [X] Sí (stop inmediato)
    - [ ] Con slide
    - [ ] Tu respuesta: _____________

60. **¿El sistema de IA corre en thread separado?**
    - [ ] No
    - [X] No (mismo thread)
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (81-100, responde con tu opción)

61. **¿El código tiene docstrings en todas las clases?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

62. **¿Formato de docstrings?**
    - [X] Google style
    - [ ] NumPy style
    - [ ] Tu respuesta: _____________

63. **¿Hay constantes hardcodeadas o en config?**
    - [X] Mayoría en config/constants
    - [ ] Hardcoded
    - [ ] Tu respuesta: _____________

64. **¿El código usa enumerate o range para loops?**
    - [X] enumerate cuando hay índice
    - [ ] range siempre
    - [ ] Tu respuesta: _____________

65. **¿Se usan type aliases (TypeVar)?**
    - [ ] No
    - [X] Sí para vectores, posições
    - [ ] Tu respuesta: _____________

66. **¿Los vectores usan tuplas o clase Vector2?**
    - [X] pygame.Vector2
    - [ ] Tuplas
    - [ ] Tu respuesta: _____________

67. **¿El código usa constantes para teclas (pygame constants)?**
    - [X] Sí (K_w, K_ESCAPE, etc.)
    - [ ] Strings
    - [ ] Tu respuesta: _____________

68. **¿Se usa pygame.sprite.Sprite o clase propia?**
    - [X] Clase propia basada en Sprite
    - [ ] Sprite directamente
    - [ ] Tu respuesta: _____________

69. **¿Sistema de grupos de sprites?**
    - [X] Sí (player, enemies, walls, etc.)
    - [ ] No
    - [ ] Tu respuesta: _____________

70. **¿Cómo se carga el tilemap?**
    - [X] CSV → array → Sprite Group
    - [ ] Directo a render
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (101-120, responde con tu opción)

71. **¿Los mapas CSV se validan antes de cargar?**
    - [X] Sí (dimensiones, caracteres válidos)
    - [ ] No
    - [ ] Tu respuesta: _____________

72. **¿Qué pasa con caracteres inválidos en el mapa?**
    - [ ] Se ignoran (como suelo)
    - [X] Error
    - [ ] Tu respuesta: _____________

73. **¿Las puertas tienen sprites de abierto/cerrado?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

74. **¿Las puertas tienen animación de abrir/cerrar?**
    - [X] Sí (deslizamiento)
    - [ ] Cambio instantáneo
    - [ ] Tu respuesta: _____________

75. **¿Duración de animación de puerta?**
    - [X] 0.5 segundos
    - [ ] 1 segundo
    - [ ] Tu respuesta: _____________

76. **¿Las puertas bloquean al jugador mientras se abren?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

77. **¿Los enemigos pueden atravesar puertas abiertas?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

78. **¿Los objetos en el suelo se pueden recoger mientras el enemigo chasea?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________

79. **¿Hay cooldown entre recogen objeto y puede equipar?**
    - [X] No
    - [ ] Sí
    - [ ] Tu respuesta: _____________

80. **¿El jugador puede atacar mientras se mueve?**
    - [X] Sí
    - [ ] No
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (121-140, responde con tu opción)

81. **¿Hay cooldown entre ataques del jugador?**
    - [X] Sí (determinado por arma)
    - [ ] No
    - [ ] Tu respuesta: _____________

82. **¿El ataque puede fallar (miss)?**
    - [X] No (siempre hit si en rango)
    - [ ] Sí (por animación)
    - [ ] Tu respuesta: _____________

83. **¿Hay knockback al recibir daño?**
    - [X] No
    - [ ] Sí
    - [ ] Tu respuesta: _____________

84. **¿Los enemigos hacen knockback al morir?**
    - [ ] No
    - [X] No
    - [ ] Tu respuesta: _____________

85. **¿Hay pantalla de "Level Complete" entre niveles?**
    - [ ] No (solo transición negra)
    - [X] Sí
    - [ ] Tu respuesta: _____________

86. **¿Se muestra el tiempo tardado en completar el nivel?**
    - [ ] No
    - [X] Si
    - [ ] Tu respuesta: _____________

87. **¿Hay contador de muertes durante el juego?**
    - [ ] No
    - [X] No
    - [ ] Tu respuesta: _____________

88. **¿El juego guarda estadísticas (muertes, tiempo)?**
    - [ ] No
    - [X] Si
    - [ ] Tu respuesta: _____________

89. **¿Qué muestra la pantalla de "Game Over"?**
    - [X] Texto "GAME OVER" + reinicio automático
    - [ ] Estadísticas
    - [ ] Tu respuesta: _____________

90. **¿Qué muestra la pantalla de "Victoria"?**
    - [X] Texto "YOU ESCAPED!" + reinicio
    - [ ] Estadísticas
    - [ ] Tu respuesta: _____________


### Nuevas Preguntas (141-160, responde con tu opción)

91. **¿Las opciones se pueden cambiar durante el juego?**
    - [X] Sí (menú pausa)
    - [ ] Solo desde menú principal
    - [ ] Tu respuesta: _____________

92. **¿El cambio de fullscreen requiere reinicio?**
    - [X] No
    - [ ] Sí
    - [ ] Tu respuesta: _____________

93. **¿El cambio de velocidad de giro requiere reinicio?**
    - [ ] Sí
    - [X] No
    - [ ] Tu respuesta: _____________

94. **¿Hay atajos de teclado para las opciones?**
    - [ ] No
    - [X] No
    - [ ] Tu respuesta: _____________

95. **¿El juego responde a eventos de ventana (minimize, focus)?**
    - [ ] Sí (auto-pausa al perder focus)
    - [X] No
    - [ ] Tu respuesta: _____________

96. **¿El juego guarda el estado al cerrar?**
    - [X] No
    - [ ] Sí
    - [ ] Tu respuesta: _____________

97. **¿Qué pasa si se cierra durante un nivel?**
    - [X] Se pierde todo el progreso
    - [ ] Se guarda posición
    - [ ] Tu respuesta: _____________

98. **¿El juego tiene iconocustom?**
    - [X] No (default de Pygame)
    - [ ] Sí
    - [ ] Tu respuesta: _____________

99. **¿El ejecutable tiene nombre específico?**
    - [X] escape_the_dungeon.exe / .app
    - [ ] game.exe
    - [ ] Tu respuesta: _____________

100. **¿El proyecto usa algún template o boilerplate?**
   - [X] No (desde cero)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

---

## 7. Nuevas Preguntas (101-120)

101. **¿El código tiene type hints en funciones públicas?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

102. **¿Se usa frozen dataclass para constantes?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________

103. **¿Hay Exception personalizada para el juego?**
   - [X] Sí (GameException base)
   - [ ] No
   - [ ] Tu respuesta: _____________

104. **¿El juego maneja errores de archivos con try/except específico?**
   - [X] Sí (LoggedException)
   - [ ] No
   - [ ] Tu respuesta: _____________

105. **¿Los colores se definen en constants.py?**
   - [X] Sí
   - [ ] En cada módulo
   - [ ] Tu respuesta: _____________

106. **¿Las constantes físicas (GRAVITY, FRICTION) están en config?**
   - [X] Sí
   - [ ] Hardcoded
   - [ ] Tu respuesta: _____________

107. **¿El juego tiene estado global (GameState singleton)?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________

108. **¿Cómo se pasa el estado entre escenas?**
   - [X] Parámetro en función change_scene
   - [ ] Global
   - [ ] Tu respuesta: _____________

109. **¿Las escenas heredan de clase base Scene?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

110. **¿Sistema de меню usa sistema de escenas?**
   - [X] Sí (MenuScene, GameScene, etc.)
   - [ ] No
   - [ ] Tu respuesta: _____________

111. **¿Las transiciones entre escenas son inmediatas?**
   - [X] No (con fade)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

112. **¿Duración del fade entre escenas?**
   - [X] 0.5 segundos
   - [ ] 1 segundo
   - [ ] Tu respuesta: _____________

113. **¿El player tiene clase dedicada (Player class)?**
   - [X] Sí
   - [ ] No (Entity genérica)
   - [ ] Tu respuesta: _____________

114. **¿El player tiene componentes (movement, combat)?**
   - [X] Sí (composición)
   - [ ] No (monolítica)
   - [ ] Tu respuesta: _____________

115. **¿Los enemies tienen clase dedicada (Enemy class)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

116. **¿Enemy hereda de Entity base?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

117. **¿Sistema de items usa clase Inventory?**
   - [X] Sí
   - [ ] No (solo array)
   - [ ] Tu respuesta: _____________

118. **¿Inventory es parte del player o global?**
   - [X] Parte del player
   - [ ] Global
   - [ ] Tu respuesta: _____________

119. **¿Las armas tienen clase Weapon?**
   - [X] Sí
   - [ ] No (dict)
   - [ ] Tu respuesta: _____________

120. **¿Las armaduras tienen clase Armor?**
   - [X] Sí
   - [ ] No (dict)
   - [ ] Tu respuesta: _____________


## 8. Nuevas Preguntas (121-140)

121. **¿Weapon y Armor heredan de Item base?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

122. **¿Los JSON de items tienen estructura específica?**
   - [X]Sí {"name": str, "damage": int, "speed": float, ...}
   - [ ] Libre
   - [ ] Tu respuesta: _____________

123. **¿Los sprites de items se cargan por nombre?**
   - [X]Sí (item_{name}.png)
   - [ ] Por ID
   - [ ] Tu respuesta: _____________

124. **¿Los mapas CSV tienen header con metadatos?**
   - [ ] No
   - [X] Sí (# width:48, height:48)
   - [ ] Tu respuesta: _____________

125. **¿El parser de mapas es función separada?**
   - [X] Sí (parse_map_csv)
   - [ ] En línea
   - [ ] Tu respuesta: _____________

126. **¿El renderer tiene método draw_map?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

127. **¿El renderer tiene método draw_entities?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

128. **¿El renderer tiene método draw_ui?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

129. **¿El input se procesa en input_system?**
   - [X] Sí
   - [ ] En game loop
   - [ ] Tu respuesta: _____________

130. **¿Input system devuelve lista de acciones?**
   - [X] Sí (key_down, key_up events)
   - [ ] Directamente ejecuta
   - [ ] Tu respuesta: _____________

131. **¿El physics system actualiza posiciones?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

132. **¿Collision system usa quadtree?**
   - [ ] No
   - [X] No (con 48x48 es innecesario)
   - [ ] Tu respuesta: _____________

133. **¿Collision system es parte de physics?**
   - [X] Sí (check_collisions)
   - [ ] Separate
   - [ ] Tu respuesta: _____________

134. **¿AI system actualiza estados de enemigos?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

135. **¿AI system usa máquina de estados?**
   - [X] Sí (PatrolState, ChaseState, AttackState)
   - [ ] If/else
   - [ ] Tu respuesta: _____________

136. **¿Combat system calcula daño?**
   - [X] Sí
   - [ ] En entity
   - [ ] Tu respuesta: _____________

137. **¿Combat system aplica daño a entidades?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

138. **¿Hay sistema de audio independiente?**
   - [X] Sí (AudioSystem class)
   - [ ] No
   - [ ] Tu respuesta: _____________

139. **¿AudioSystem tiene método play_sound?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

140. **¿AudioSystem tiene método play_music?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________


## 9. Nuevas Preguntas (141-160)

141. **¿Los sonidos se cargan lazy (on demand)?**
   - [X] Sí
   - [ ] Al inicio
   - [ ] Tu respuesta: _____________

142. **¿Música hace loop automáticamente?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

143. **¿El volumen es global o por canal?**
   - [X] Global
   - [ ] Por canal
   - [ ] Tu respuesta: _____________

144. **¿Hay efecto de sonido para pasos?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

145. **¿Hay efecto de sonido para abrir puerta?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

146. **¿Hay efecto de sonido para recoger item?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

147. **¿Hay efecto de sonido para transición de nivel?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

148. **¿El juego muestra cursor custom?**
   - [ ] No
   - [X] No (default)
   - [ ] Tu respuesta: _____________

149. **¿Cursor se oculta durante el juego?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________

150. **¿El juego permite restart rápido (tecla R)?**
   - [X] No, desde el menu con el botón restart.
   - [ ] Sí
   - [ ] Tu respuesta: _____________

151. **¿Hay debug overlay (FPS, position)?**
   - [ ] No
   - [X] Sí (toggle with F3)
   - [ ] Tu respuesta: _____________

152. **¿El código usa logging.info para eventos importantes?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

153. **¿logging.debug se usa para información de desarrollo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

154. **¿Los errores se loguean con traceback completo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

155. **¿Hay mensajes de inicio al запускать el juego?**
   - [X] Sí (Logging info)
   - [ ] No
   - [ ] Tu respuesta: _____________

156. **¿El juego muestra versión en algún lado?**
   - [X] No
   - [ ] Sí (menú)
   - [ ] Tu respuesta: _____________

157. **¿La versión se guarda en __init__.py o config?**
   - [X] En config (VERSION)
   - [ ] __init__.py
   - [ ] Tu respuesta: _____________

158. **¿El código usa assertions para debug?**
   - [ ] No
   - [X] Sí (en développement)
   - [ ] Tu respuesta: _____________

159. **¿Las constantes numéricas usan mayúsculas?**
   - [X] Sí (SCREEN_WIDTH, TILE_SIZE)
   - [ ] No
   - [ ] Tu respuesta: _____________

160. **¿Las constantes se agrup an en módulos (constants.py)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________


## 10. Nuevas Preguntas (161-180)

161. **¿El juego usa constantes para rutas de archivos?**
   - [X] Sí (PATHS.DATA, PATHS.SPRITES)
   - [ ] Hardcoded strings
   - [ ] Tu respuesta: _____________

162. **¿Las rutas se definen en config paths?**
   - [X] Sí
   - [ ] En cada módulo
   - [ ] Tu respuesta: _____________

163. **¿El juego detecta assets faltantes al inicio?**
   - [X] Sí (con warning)
   - [ ] No
   - [ ] Tu respuesta: _____________

164. **¿Qué hace si falta un archivo de sprite?**
   - [X] Usa color por defecto
   - [ ] Error
   - [ ] Tu respuesta: _____________

165. **¿Qué hace si falta un archivo JSON de nivel?**
   - [X] Error (fatal)
   - [ ] Skip nivel
   - [ ] Tu respuesta: _____________

166. **¿El juego tiene modo a prueba de errores (graceful degradation)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

167. **¿Las excepciones se manejan en game loop try/except?**
   - [X] Sí (top-level)
   - [ ] No
   - [ ] Tu respuesta: _____________

168. **¿El código usa f-strings para formateo?**
   - [X] Sí
   - [ ] .format()
   - [ ] Tu respuesta: _____________

169. **¿Los imports usan rutas absolutas desde src?**
   - [X] Sí (from src.core import)
   - [ ] Relative
   - [ ] Tu respuesta: _____________

170. **¿Los módulos tienen __all__ definido?**
   - [ ] No
   - [X] Sí (en módulos principales)
   - [ ] Tu respuesta: _____________

171. **¿Se usa __version__ en algún módulo?**
   - [ ] No
   - [X] No
   - [ ] Tu respuesta: _____________

172. **¿El juego tiene archivo README?**
   - [ ] No por ahora
   - [X] Sí
   - [ ] Tu respuesta: _____________

173. **¿El proyecto tiene LICENSE?**
   - [ ] No
   - [X] MIT
   - [ ] Tu respuesta: _____________

174. **¿Hay .gitignore?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

175. **¿El .gitignore incluye __pycache__ y .pyc?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

176. **¿El .gitignore incluye archivos de IDE?**
   - [X] Sí (.vscode, .idea)
   - [ ] No
   - [ ] Tu respuesta: _____________

177. **¿Se hace commit con mensajes en español o inglés?**
   - [X] Inglés
   - [ ] Español
   - [ ] Tu respuesta: _____________

178. **¿Los commits siguen conventional commits?**
   - [ ] No
   - [X] Si
   - [ ] Tu respuesta: _____________

179. **¿Hay branch develop/main?**
   - [ ] Solo master/main
   - [X] develop + main
   - [ ] Tu respuesta: _____________

180. **¿El workflow de git es simple (commit - push)?**
   - [X] Sí
   - [ ] Con PRs
   - [ ] Tu respuesta: _____________


## 11. Nuevas Preguntas (181-200)

181. **¿Se usa pre-commit hook?**
   - [ ] No
   - [X] No
   - [ ] Tu respuesta: _____________

182. **¿El código pasa pylint con score > 8?**
   - [X] Sí (> 8)
   - [ ] No
   - [ ] Tu respuesta: _____________

183. **¿Hay ruff o black para formateo?**
   - [X] ruff
   - [ ] black
   - [ ] Tu respuesta: _____________

184. **¿ruff se configura en pyproject.toml?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

185. **¿Los tests se ejecutan con uv run pytest?**
   - [X] Sí
   - [ ] pytest directo
   - [ ] Tu respuesta: _____________

186. **¿Los tests tienen coverage mínimo?**
   - [ ] No
   - [X] No
   - [ ] Tu respuesta: _____________

187. **¿Los tests se agrupan por módulo (tests/core, tests/entities)?**
   - [X] Sí
   - [ ] tests/ general
   - [ ] Tu respuesta: _____________

188. **¿Los fixtures se usan en tests?**
   - [X] Sí (conftest.py)
   - [ ] No
   - [ ] Tu respuesta: _____________

189. **¿Los mocks se usan para外部 dependencies?**
   - [X] Sí (para archivos, audio)
   - [ ] No
   - [ ] Tu respuesta: _____________

190. **¿Los tests de integración existen?**
   - [ ] No
   - [X] Si
   - [ ] Tu respuesta: _____________


## 12. Nuevas Preguntas (201-220)

191. **¿El renderer usa pygame.Surface?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

192. **¿La pantalla se crea con pygame.display.set_mode?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

193. **¿El juego usa display flip o update?**
   - [X] pygame.display.flip()
   - [ ] pygame.display.update()
   - [ ] Tu respuesta: _____________

194. **¿clock.tick se llama con FPS constante?**
   - [X] Sí (clock.tick(60))
   - [ ] No
   - [ ] Tu respuesta: _____________

195. **¿pygame.init se llama al inicio?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

196. **¿pygame.quit se llama al cerrar?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

197. **¿El juego usa pygame.font?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

198. **¿Las fuentes se cargan una vez (cache)?**
   - [X] Sí
   - [ ] Cada vez
   - [ ] Tu respuesta: _____________

199. **¿El juego tiene fuente por defecto si no hay archivo?**
   - [X] Sí (pygame.font.Font(None, size))
   - [ ] No
   - [ ] Tu respuesta: _____________

200. **¿Los textos se renderizan a surface y se guardan?**
   - [X] Sí (cache)
   - [ ] Cada frame
   - [ ] Tu respuesta: _____________


## 13. Nuevas Preguntas (221-240)

201. **¿Las superficies de texto tienen antialias activo?**
   - [ ] Sí
   - [ ] No
   - [X] Tu respuesta: Configurable en opciones Si/No - Por defecto Si.

202. **¿El sistema de UI usa botones con rectángulos?**
   - [X] Sí
   - [ ] Sprites
   - [ ] Tu respuesta: _____________

203. **¿Los botones tienen estado (hover, click)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

204. **¿Los botones tienen sonido al hacer click?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

205. **¿El menú tiene animación de hover?**
   - [ ] No
   - [X] Si
   - [ ] Tu respuesta: _____________

206. **¿Los items del menú se navegables con flechas?**
   - [X] Sí
   - [ ] Solo mouse
   - [ ] Tu respuesta: _____________

207. **¿El menú permite seleccionar con Enter?**
   - [X] Sí
   - [ ] Solo click
   - [ ] Tu respuesta: _____________

208. **¿El menú tiene opción de restart?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

209. **¿El menú de pause tiene las mismas opciones que el main?**
   - [X] Sí (Resume + Restart + Options + Quit)
   - [ ] Diferentes
   - [ ] Tu respuesta: _____________

210. **¿El juego detecta cierre de ventana (pygame.QUIT)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________


## 14. Nuevas Preguntas (241-260)

211. **¿El juego responde a KEYDOWN y KEYUP por separado?**
   - [X] Sí
   - [ ] Solo KEYDOWN
   - [ ] Tu respuesta: _____________

212. **¿Las teclas se verifican con pygame.key.get_pressed()?**
   - [X] Sí (movimiento continuo)
   - [ ] No
   - [ ] Tu respuesta: _____________

213. **¿El input de movimiento usa get_pressed?**
   - [X] Sí
   - [ ] Eventos
   - [ ] Tu respuesta: _____________

214. **¿El input de acciones usa eventos (KEYDOWN)?**
   - [X] Sí (ataque, interacción)
   - [ ] get_pressed
   - [ ] Tu respuesta: _____________

215. **¿Las acciones tienen cooldown implementado?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

216. **¿El cooldown usa tiempo real (pygame.time.get_ticks)?**
   - [X] Sí
   - [ ] Frames
   - [ ] Tu respuesta: _____________

217. **¿La detección de colisiones usa pygame.sprite collide?**
   - [X] Sí
   - [ ] custom
   - [ ] Tu respuesta: _____________

218. **¿collide_rect se usa con groups?**
   - [X] Sí (spritecollide)
   - [ ] Manual
   - [ ] Tu respuesta: _____________

219. **¿Los grupos de sprites tienen汞?**
   - [X] Sí (player_group, enemy_group, wall_group)
   - [ ] No
   - [ ] Tu respuesta: _____________

220. **¿Los sprites usan método update()?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________


## 15. Nuevas Preguntas (261-280)

221. **¿Los sprites tienen método draw()?**
   - [X] Sí
   - [ ] No (se drawn por group)
   - [ ] Tu respuesta: _____________

222. **¿La cámara sigue al jugador?**
   - [X] Sí (Camera class)
   - [ ] No (mapa fijo)
   - [ ] Tu respuesta: _____________

223. **¿La cámara usa offset?**
   - [X] Sí (camera_offset)
   - [ ] No
   - [ ] Tu respuesta: _____________

224. **¿La cámara está centrada en el jugador?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

225. **¿La cámara tiene límites del mapa?**
   - [X] Sí (no sale del mapa)
   - [ ] No
   - [ ] Tu respuesta: _____________

226. **¿El rendering aplica offset de cámara?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

227. **¿Los tilemap tiles tienen posición en pixels o grid?**
   - [X] Pixels (grid * TILE_SIZE)
   - [ ] Grid
   - [ ] Tu respuesta: _____________

228. **¿Los NPCs tienen comportamiento específico por tipo?**
   - [X] Sí (enemy_type en JSON)
   - [ ] No
   - [ ] Tu respuesta: _____________

229. **¿Los items en mapa se representan como sprites?**
   - [X] Sí
   - [ ] No (rectángulos)
   - [ ] Tu respuesta: _____________

230. **¿Los items tienen interacción por proximidad?**
   - [X] Sí (distancia < 2 tiles)
   - [ ] No
   - [ ] Tu respuesta: _____________


## 16. Nuevas Preguntas (281-300)

231. **¿Los items se equipan automáticamente al recoger?**
   - [X] Sí
   - [ ] No (separar pickup/equip)
   - [ ] Tu respuesta: _____________

232. **¿Al equipar se hace drop del item anterior?**
   - [X] Sí (en la misma celda)
   - [ ] No
   - [ ] Tu respuesta: _____________

233. **¿Los items tirados se convierten en sprites en el suelo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

234. **¿El drop de items crea entity en el mundo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

235. **¿Las puertas se representan como sprites animado?**
   - [X] Sí (abierto/cerrado)
   - [ ] No
   - [ ] Tu respuesta: _____________

236. **¿Las puertas tienen estado (is_open)?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

237. **¿Las puertas bloquean colisión cuando closed?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

238. **¿Las puertas permiten paso cuando open?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

239. **¿El player puede abrir puerta desde distancia?**
   - [ ] Sí (2 tiles)
   - [X] No (solo adyacente)
   - [ ] Tu respuesta: _____________

240. **¿Las puertas bloquean línea de visión?**
   - [X] Sí (cuando closed)
   - [ ] No
   - [ ] Tu respuesta: _____________


## 17. Nuevas Preguntas (301-320)

241. **¿Los enemigos tienen campo de visión cónico?**
   - [X] Sí (120° delant)
   - [ ] No (360°)
   - [ ] Tu respuesta: _____________

242. **¿El enemy detecta al jugador si está en campo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

243. **¿El enemy tiene distancia de detección específica?**
   - [X] Sí (varía por nivel)
   - [ ] No
   - [ ] Tu respuesta: _____________

244. **¿El enemy usa pathfinding hacia el jugador?**
   - [ ] No (línea directa)
   - [X] Sí (A*)
   - [ ] Tu respuesta: _____________

245. **¿El enemy se detiene si hay pared en medio?**
   - [X] Sí (no puede ver)
   - [ ] No
   - [ ] Tu respuesta: _____________

246. **¿El enemy vuelve a patrol si pierde de vista al jugador?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

247. **¿El enemy tiene tiempo de persecución limitado?**
   - [ ] No
   - [X] Si
   - [ ] Tu respuesta: _____________

248. **¿El enemy ataca automáticamente al chasear?**
   - [X] Sí (cuando en rango)
   - [ ] No
   - [ ] Tu respuesta: _____________

249. **¿El ataque del enemy tiene animación?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

250. **¿El enemy hace daño durante animación o al final?**
   - [X] Al final de la animación
   - [ ] Durante
   - [ ] Tu respuesta: _____________


## 18. Nuevas Preguntas (321-340)

251. **¿El daño del enemy se muestra visualmente?**
   - [X] Sí (flash rojo)
   - [ ] No
   - [ ] Tu respuesta: _____________

252. **¿El player tiene frames de invulnerabilidad después de recibir daño?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

253. **¿El player puede morir de un ataque?**
   - [X] Sí (100% vida, depende del arma)
   - [ ] No
   - [ ] Tu respuesta: _____________

254. **¿Al morir el player se muestra animación?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

255. **¿Después de animación de muerte hay transición a game over?**
   - [X] Sí (2 segundos)
   - [ ] No
   - [ ] Tu respuesta: _____________

256. **¿El game over muestra el nivel donde murió?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________

257. **¿Al completar nivel hay transición a siguiente?**
   - [X] Sí (pantalla negra + nombre siguiente nivel)
   - [ ] No
   - [ ] Tu respuesta: _____________

258. **¿El juego muestra "Level Complete" con tiempo?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________

259. **¿Al completar nivel 5 hay pantalla de victoria?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

260. **¿Después de victoria se guarda score/stats?**
   - [ ] No
   - [X] Si - luego se pueden ver en una tabla, que aparece comobotón entre ocpiones y cerrar el juego, donde se mostrará el tiempo que se tardó en cada mundo, mostrando como el primero el menor tiempo con el maximo numero de mundos recorridos. 
   - [ ] Tu respuesta: _____________


## 19. Nuevas Preguntas (341-360)

261. **¿Después de victoria hay opción de jugar de nuevo?**
   - [X] Sí (reinicio automático tras 5s)
   - [ ] No
   - [ ] Tu respuesta: _____________

262. **¿El juego tiene sistema de guardado de opciones?**
   - [X] Sí (JSON)
   - [ ] No
   - [ ] Tu respuesta: _____________

263. **¿El archivo de opciones se guarda en home directory?**
   - [X] No (mismo directorio que el juego)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

264. **¿Las opciones incluyen volumen?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

265. **¿Las opciones incluyen velocidad de giro?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

266. **¿Las opciones incluyen fullscreen?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

267. **¿Las opciones se cargan al iniciar el juego?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

268. **¿Las opciones se guardan al cambiar en opciones?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

269. **¿El juego tiene sistema de logros/achievements?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

270. **¿El juego tiene leaderboard?**
   - [ ] No
   - [X] Sí
   - [ ] Tu respuesta: _____________


## 20. Nuevas Preguntas (361-380)

271. **¿El juego tiene económico/moneda?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

272. **¿Los enemies solt an предметы al morir?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

273. **¿El juego tiene crafting?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

274. **¿El juego tiene inventario extenso (más de 2 items)?**
   - [X] No (solo arma + armadura)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

275. **¿El jugador puede comprar items en el juego?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

276. **¿Hay NPCs merchants en el juego?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

277. **¿El juego tiene quests/misiones?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

278. **¿El juego tiene tiempo día/noche?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

279. **¿El juego tiene clima (lluvia, nieve)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

280. **¿El juego tiene ciclos de nivel (entrar, salir)?**
   - [X] Solo lineal (nivel 1 a 5)
   - [ ] No
   - [ ] Tu respuesta: _____________


## 21. Nuevas Preguntas (381-400)

281. **¿El juego tiene secretos/áreas ocultas?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

282. **¿El juego tiene Easter eggs?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

283. **¿Los niveles tienen tamaño fijo?**
   - [X] Sí (48x48)
   - [ ] Variable
   - [ ] Tu respuesta: _____________

284. **¿Los niveles tienen biomas específicos?**
   - [X] Sí (Dungeon, Castle, Camp, Forest, Mountain)
   - [ ] No
   - [ ] Tu respuesta: _____________

285. **¿Cada bioma tiene sprites diferentes de paredes/suelo?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

286. **¿Los sprites de tiles se cargan dinámicamente por nivel?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

287. **¿Los decorados varían por bioma?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

288. **¿Las puertas tienen sprites específicos por contexto?**
   - [X] Sí (madera para dungeon, piedra para castle)
   - [ ] No
   - [ ] Tu respuesta: _____________

289. **¿Los items tienen rarity (común, raro, épico)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

290. **¿Los items tienen nivel requerido?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________


## 22. Nuevas Preguntas (401-420)

291. **¿Los items tienen estadísticas adicionales (durabilidad)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

292. **¿Los items pueden mejorarse (upgrades)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

293. **¿Hay sistema de runas/gemas?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

294. **¿El juego tiene habilidades activas del jugador?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

295. **¿El juego tiene habilidades pasivas?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

296. **¿El jugador tiene clase/rol específico?**
   - [X] No (genérico)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

297. **¿El juego permite crear personaje?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

298. **¿Los enemies tienen tipos diferentes (orcos, esqueletos)?**
   - [X] No (solo humanos)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

299. **¿Los enemies tienen nombre específico?**
   - [X] No (genéricos)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

300. **¿Los enemies tienen level/stats variables?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________


## 23. Nuevas Preguntas (421-440)

301. **¿Los enemies tienen HP visible?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

302. **¿El jugador ve HP de enemy al atacarlo?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

303. **¿El ataque del enemigo tiene sonido?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

304. **¿El ataque del jugador tiene sonido?**
   - [X] Procedural si no hay MP3
   - [ ] No
   - [ ] Tu respuesta: _____________

305. **¿La música cambia por situación (combate, exploración)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

306. **¿La música se detiene al pausar?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

307. **¿La música se reanuda al despausar?**
   - [X] Sí
   - [ ] No
   - [ ] Tu respuesta: _____________

308. **¿El juego tiene subtítulos/dialogos?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

309. **¿El juego tiene historia introductoria?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

310. **¿El juego tiene final alternativo?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________


## 24. Nuevas Preguntas (441-460)

311. **¿El juego es jugable sin sonido?**
   - [X] Sí (totalmente)
   - [ ] No
   - [ ] Tu respuesta: _____________

312. **¿El juego funciona sin mouse?**
   - [X] Sí (teclado completo)
   - [ ] No
   - [ ] Tu respuesta: _____________

313. **¿El juego funciona solo con mouse?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

314. **¿El juego detecta gamepad/control?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

315. **¿El juego tiene configuración de controles?**
   - [X] No (fijos)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

316. **¿El juego soporta multiplayer?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

317. **¿El juego tiene modo cooperativo?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

318. **¿El juego tiene modo versus?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

319. **¿El juego tiene procedurally generated levels?**
   - [X] No (手功制作)
   - [ ] Sí
   - [ ] Tu respuesta: _____________

320. **¿Los niveles tienen duración estimada?**
   - [X] No (exploración libre)
   - [ ] Sí
   - [ ] Tu respuesta: _____________


## 25. Nuevas Preguntas (461-480)

321. **¿El juego tiene sistema de logros/trofeos?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

322. **¿El juego tiene sistema de estadísticas globales?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

323. **¿El juego guarda historial de partidas?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

324. **¿El juego tiene modo practice/training?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

325. **¿El juego tiene nivel tutorial?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

326. **¿El juego tiene hints/tips durante juego?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

327. **¿El juego tiene secretos desbloqueables?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

328. **¿El juego tiene contenido desbloqueable?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

329. **¿El juego tiene dificultades adicionales (hard, nightmare)?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

330. **¿El juego tiene New Game Plus?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________


## 26. Nuevas Preguntas (481-500)

331. **¿El juego tiene DLCs/expansiones?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

332. **¿El juego tiene microtransacciones?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

333. **¿El juego está en acceso anticipado?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

334. **¿El juego tiene soporte para mods?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

335. **¿El juego tiene API para scripting?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

336. **¿El código está disponible en repositorio público?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

337. **¿El juego tiene página weboficial?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

338. **¿El juego tiene comunidad/foros?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

339. **¿El juego tiene actualizaciones regulares?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________

340. **¿El juego tiene soporte técnico?**
   - [X] No
   - [ ] Sí
   - [ ] Tu respuesta: _____________
