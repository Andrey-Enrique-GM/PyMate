from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap

class PetWindow(QWidget):
    def __init__(self, sprite_path: str):
        super().__init__()
        
        # Dimensiones extraídas del config.txt
        self.frame_width = 350
        self.frame_height = 350

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.set_sprite(sprite_path)
        self.drag_position = None

    def set_sprite(self, image_path: str):
        full_pixmap = QPixmap(image_path)
        
        if not full_pixmap.isNull():
            # Recorta el cuadro inicial [X:0, Y:0, Ancho:350, Alto:350]
            cropped_pixmap = full_pixmap.copy(QRect(0, 0, self.frame_width, self.frame_height))
            
            self.label.setPixmap(cropped_pixmap)
            self.resize(self.frame_width, self.frame_height)
        else:
            print(f"Error cargando: {image_path}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None