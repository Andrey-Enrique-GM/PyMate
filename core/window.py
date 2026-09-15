from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from core.sprite_animator import SpriteAnimator

class PetWindow(QWidget):
    def __init__(self, sprite_path: str, total_frames: int = 340, fps: int = 60):
        super().__init__()

        # Configuración de la ventana transparente
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

        # Inicializar animador para 'idle'
        self.animator = SpriteAnimator(
            sprite_path=sprite_path,
            total_frames=total_frames,
            frame_width=350,
            frame_height=350,
            columns=10
        )

        # Configurar temporizador de reproducción (FPS)
        interval_ms = int(1000 / fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(interval_ms)

        self.drag_position = None

    def update_animation(self):
        pixmap = self.animator.get_next_frame()
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.resize(pixmap.size())

    # --- Eventos para mover la ventana con el mouse ---
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