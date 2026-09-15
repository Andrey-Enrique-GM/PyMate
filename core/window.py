from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from core.sprite_animator import SpriteAnimator

class PetWindow(QWidget):
    def __init__(self, sprite_path: str, total_frames: int = 340, target_size: int = 230, fps: int = 24):
        super().__init__()

        self.target_size = target_size

        # Configurar la ventana transparente y flotante
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Configuración del QLabel fija a 230px
        self.label = QLabel(self)
        self.label.setFixedSize(self.target_size, self.target_size)
        self.label.setScaledContents(True)  # Escala la imagen original directo al marco
        self.layout.addWidget(self.label)

        self.resize(self.target_size, self.target_size)

        # Animador
        self.animator = SpriteAnimator(
            sprite_path=sprite_path,
            total_frames=total_frames,
            frame_width=350,
            frame_height=350,
            columns=10
        )

        interval_ms = int(1000 / fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(interval_ms)

        self.is_dragging = False
        self.drag_offset = QPoint()

    def update_animation(self):
        pixmap = self.animator.get_next_frame()
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)

    # --- Eventos para arrastrar ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            event.accept()