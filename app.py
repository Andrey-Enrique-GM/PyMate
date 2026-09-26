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

    # Icono para la bandeja del sistema
    idle_data = character.get_animation_data("idle")
    full_pixmap = QPixmap(idle_data["path"])
    
    if not full_pixmap.isNull():
        icon_pixmap = full_pixmap.copy(0, 0, idle_data["frame_width"], idle_data["frame_height"])
        tray_icon = QIcon(icon_pixmap)
    else:
        tray_icon = QIcon()

    tray = QSystemTrayIcon(tray_icon, app)
    tray.setToolTip(f"PyMate - {character.name}")

    # Menú del tray icon
    menu = QMenu()
    close_action = menu.addAction("Cerrar")
    
    # Reproduce la animación de despedida al cerrar
    close_action.triggered.connect(window.play_outro_and_exit)

    tray.setContextMenu(menu)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
