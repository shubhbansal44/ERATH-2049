from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCES_DIR = PROJECT_ROOT / "Sources"
CODE_DIR = PROJECT_ROOT / "Code"

DIGITS_DIR = SOURCES_DIR / "digits"
EFFECTS_DIR = SOURCES_DIR / "effects"
ENEMIES_DIR = SOURCES_DIR / "enemies"
FLOORS_DIR = SOURCES_DIR / "floors"
ICON_DIR = SOURCES_DIR / "icon"
OBJECTS_DIR = SOURCES_DIR / "objects"
SKY_DIR = SOURCES_DIR / "sky"
SOUNDS_DIR = SOURCES_DIR / "sounds"
WALLS_DIR = SOURCES_DIR / "walls"
WEAPONS_DIR = SOURCES_DIR / "weapons"

CREDITS_FILE = CODE_DIR / "credits.txt"
DEFAULT_SETTINGS_FILE = CODE_DIR / "default_settings.txt"
SAVED_SETTINGS_FILE = CODE_DIR / "saved_settings.txt"
SAVED_GAME_FILE = CODE_DIR / "saved_game.txt"
