import sys
from PyQt6.QtWidgets import QApplication
from core.window import PetWindow

def main():
    app = QApplication(sys.argv)

    sprite_path = "assets/SpriteSheet/GoldShip/idle.png"

    pet = PetWindow(sprite_path=sprite_path, total_frames=340, target_size=230, fps=35)
    pet.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()