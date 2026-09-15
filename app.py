import sys
from PyQt6.QtWidgets import QApplication
from core.window import PetWindow
from config import ConfigManager

def main():
    app = QApplication(sys.argv)

    cfg = ConfigManager()

    sprite_path = cfg.get_sprite_path("idle")
    
    # Extraer parámetros de la config específica del personaje
    total_frames = int(cfg.character_config.get("IDLE", 340))
    frame_width = int(cfg.character_config.get("WIDTH", 350))
    frame_height = int(cfg.character_config.get("HEIGHT", 350))
    columns = int(cfg.character_config.get("COLUMN", 10))

    # Fijamos los FPS a 35 para mantener la fluidez en cualquier personaje
    pet = PetWindow(
        sprite_path=sprite_path, 
        total_frames=total_frames,
        frame_width=frame_width,
        frame_height=frame_height,
        columns=columns,
        target_size=230, 
        fps=35
    )
    pet.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()