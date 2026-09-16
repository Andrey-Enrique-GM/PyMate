import sys
from PyQt6.QtWidgets import QApplication
from core.window import PetWindow
from core.character import Character
from config import ConfigManager



def main():
    app = QApplication(sys.argv)

    cfg = ConfigManager()
    active_char_name = cfg.active_character

    # Instancia el personaje activo
    character = Character(character_name=active_char_name)

    pet = PetWindow(
        character=character,
        target_size=230, 
        fps=35
    )
    pet.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    