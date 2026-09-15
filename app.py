import sys
from PyQt6.QtWidgets import QApplication
from core.window import PetWindow

def main():
    app = QApplication(sys.argv)

    # Ruta a la animación idle (con 340 frames)
    sprite_path = "assets/SpriteSheet/GoldShip/idle.png"

    pet = PetWindow(sprite_path=sprite_path, total_frames=340, fps=60)
    pet.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()