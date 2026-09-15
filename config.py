import os

class ConfigManager:
    def __init__(self, base_assets_path: str = "assets"):
        self.assets_path = base_assets_path
        self.global_config = {}
        self.character_config = {}
        
        self._load_global_config()
        self.active_character = self.global_config.get("START_CHAR", "GoldShip")
        self._load_character_config()

    def _parse_txt(self, file_path: str) -> dict:
        data = {}
        if not os.path.exists(file_path):
            return data
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    data[key.strip()] = value.strip()
        return data

    def _load_global_config(self):
        global_path = os.path.join(self.assets_path, "config.txt")
        self.global_config = self._parse_txt(global_path)

    def _load_character_config(self):
        char_path = os.path.join(self.assets_path, "SpriteSheet", self.active_character, "config.txt")
        self.character_config = self._parse_txt(char_path)

    def get_sprite_path(self, animation_name: str = "idle") -> str:
        return os.path.join(self.assets_path, "SpriteSheet", self.active_character, f"{animation_name}.png")