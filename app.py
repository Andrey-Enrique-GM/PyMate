import sys
from PyQt6.QtWidgets import QApplication
from core.window import PetWindow

def main():
    app = QApplication(sys.argv)

    # Ruta a la imagen PNG de Goldship dentro de la carpeta assets
    sprite_path = "assets/SpriteSheet/GoldShip/idle.png" 

    pet = PetWindow(sprite_path)
    pet.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()