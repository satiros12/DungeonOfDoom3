"""Constants for Escape the Dungeon of Doom game."""

# ==================== SCREEN ====================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SCREEN_TITLE = "Escape the Dungeon of Doom"

# ==================== TILE ====================
TILE_SIZE = 16
MAP_WIDTH = 48
MAP_HEIGHT = 48

# ==================== COLORS (GRAPHICS_SPECS) ====================
# Entity colors
COLOR_PLAYER = (0, 255, 0)  # #00FF00 - Green
COLOR_ENEMY = (255, 0, 0)  # #FF0000 - Red
COLOR_DOOR = (0, 0, 255)  # #0000FF - Blue
COLOR_DOOR_OPEN = (0, 255, 0)  # #00FF00 - Green (open door)
COLOR_ITEM = (255, 255, 0)  # #FFFF00 - Yellow
COLOR_WALL = (128, 128, 128)  # #808080 - Gray
COLOR_DECORATION = (139, 69, 19)  # #8B4513 - Brown
COLOR_EXIT = (255, 215, 0)  # #FFD700 - Gold
COLOR_FLOOR = (0, 0, 0)  # #000000 - Black

# UI colors (UX_SPECS)
UI_COLOR_BACKGROUND = (26, 26, 26)  # #1a1a1a
UI_COLOR_TEXT_PRIMARY = (201, 162, 39)  # #c9a227 - Gold
UI_COLOR_TEXT_SECONDARY = (139, 115, 85)  # #8b7355 - Brown leather
UI_COLOR_HIGHLIGHT = (255, 107, 53)  # #ff6b35 - Orange fire
UI_COLOR_BORDER = (74, 55, 40)  # #4a3728 - Dark brown
UI_COLOR_HEALTH = (204, 51, 51)  # #cc3333 - Red
UI_COLOR_HEALTH_BG = (42, 42, 42)  # #2a2a2a - Dark gray

# Menu background
MENU_BG_COLOR = (20, 20, 30)  # #14141E

# ==================== UI FONTS ====================
UI_FONT_TITLE = 48
UI_FONT_MENU = 28
UI_FONT_HUD = 18
UI_FONT_DEBUG = 14

# ==================== HUD ====================
HUD_MARGIN = 20
HUD_HEALTH_BAR_WIDTH = 200
HUD_HEALTH_BAR_HEIGHT = 20
HUD_TAB_DISPLAY_TIME = 2.0  # seconds
HUD_TAB_FADE_TIME = 0.3  # seconds

# ==================== CONTROLS ====================
# Movement
KEY_MOVE_FORWARD = "w"
KEY_MOVE_BACKWARD = "s"
KEY_MOVE_LEFT = "a"
KEY_MOVE_RIGHT = "d"

# View rotation
KEY_TURN_LEFT = "left"
KEY_TURN_RIGHT = "right"

# Actions
KEY_ATTACK = "space"
KEY_INTERACT = "e"
KEY_DROP_WEAPON = "i"
KEY_DROP_ARMOR = "j"
KEY_TOGGLE_HEALTH = "tab"
KEY_PAUSE = "escape"
KEY_DEBUG = "f3"

# ==================== TURN SPEED ====================
TURN_SPEED_MIN = 60  # degrees/second
TURN_SPEED_MAX = 120
TURN_SPEED_DEFAULT = 90
TURN_SPEED_STEP = 10

# ==================== WEAPONS (GAME_SPECS) ====================
WEAPONS = {
    "fists": {"damage_percent": 10, "speed_multiplier": 1.0},
    "sword": {"damage_percent": 25, "speed_multiplier": 0.9},
    "axe": {"damage_percent": 40, "speed_multiplier": 0.7},
    "hammer": {"damage_percent": 70, "speed_multiplier": 0.5},
}

# Weapon display names
WEAPON_NAMES = {
    "fists": "Fists",
    "sword": "Sword",
    "axe": "Axe",
    "hammer": "Hammer",
}

# ==================== ARMORS (GAME_SPECS) ====================
ARMORS = {
    "none": {"damage_reduction": 1.0, "speed_multiplier": 1.0},
    "light": {"damage_reduction": 0.75, "speed_multiplier": 0.8},
    "medium": {"damage_reduction": 0.5, "speed_multiplier": 0.6},
    "heavy": {"damage_reduction": 0.25, "speed_multiplier": 0.3},
}

# Armor display names
ARMOR_NAMES = {
    "none": "None",
    "light": "Light",
    "medium": "Medium",
    "heavy": "Heavy",
}

# ==================== COMBAT ====================
BACKSTAB_DAMAGE_BONUS = 0.25  # +25% damage from behind
DODGE_WINDOW = 0.3  # seconds

# ==================== ENEMIES ====================
ENEMY_STATES = {
    "PATROL": "patrol",
    "CHASE": "chase",
    "ATTACK": "attack",
}

ENEMY_SPEED = 2.0  # cells/second
ENEMY_FOV = 120  # degrees
ENEMY_ATTACK_RANGE = 1  # cell
ENEMY_ATTACK_COOLDOWN = 1.0  # seconds
ENEMY_DAMAGE_TO_PLAYER = 0.1  # 10% of max health

# ==================== LEVELS (GAME_SPECS) ====================
LEVELS = {
    1: {"name": "Dungeon", "detection_radius": 5},
    2: {"name": "Castle", "detection_radius": 6},
    3: {"name": "Camp", "detection_radius": 7},
    4: {"name": "Forest", "detection_radius": 8},
    5: {"name": "Mountain Pass", "detection_radius": 9},
}

# Level display names (UX_SPECS)
LEVEL_NAMES = {
    1: "DUNGEON",
    2: "CASTLE",
    3: "CAMP",
    4: "FOREST",
    5: "MOUNTAIN PASS",
}

# ==================== ITEMS PER LEVEL ====================
ITEMS_PER_LEVEL = {
    1: {"weapons": 2, "armors": 2},
    2: {"weapons": 2, "armors": 2},
    3: {"weapons": 2, "armors": 2},
    4: {"weapons": 0, "armors": 0},
    5: {"weapons": 0, "armors": 0},
}

# ==================== TRANSITIONS ====================
TRANSITION_BLACK_TIME = 2.0  # seconds
TRANSITION_NAME_TIME = 2.0  # seconds
GAMEOVER_DISPLAY_TIME = 2.0  # seconds
VICTORY_DISPLAY_TIME = 5.0  # seconds
