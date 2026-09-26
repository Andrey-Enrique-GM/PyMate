import sys
from config import ConfigManager
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from core.character import Character
from core.window import PetWindow



def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Carga el personaje activo y ventana
    cfg = ConfigManager()
    active_char_name = cfg.active_character
    character = Character(character_name=active_char_name)
    window = PetWindow(character)
    window.show()

    # Obtiene el primer frame de IDLE para usarlo como icono de la bandeja
    idle_data = character.get_animation_data("idle")
    full_pixmap = QPixmap(idle_data["path"])
    
    if not full_pixmap.isNull():
        # Recortamos exactamente el primer cuadro (columna 0, fila 0)
        icon_pixmap = full_pixmap.copy(0, 0, idle_data["frame_width"], idle_data["frame_height"])
        tray_icon = QIcon(icon_pixmap)
    else:
        tray_icon = QIcon()

    # Crea el SystemTrayIcon en la barra de tareas
    tray = QSystemTrayIcon(tray_icon, app)
    tray.setToolTip(f"PyMate - {character.name}")

    # Crea el menú contextual (Clic derecho en el icono)
    menu = QMenu()
    close_action = menu.addAction("Cerrar")
    close_action.triggered.connect(app.quit)

    tray.setContextMenu(menu)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
