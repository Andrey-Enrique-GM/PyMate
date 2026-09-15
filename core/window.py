from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from core.sprite_animator import SpriteAnimator

class PetWindow(QWidget):
    def __init__(self, sprite_path: str, total_frames: int, frame_width: int, frame_height: int, columns: int, target_size: int = 230, fps: int = 16):
        super().__init__()

        self.target_size = target_size

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
        self.label.setFixedSize(self.target_size, self.target_size)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)

        self.resize(self.target_size, self.target_size)

        # Usamos las dimensiones exactas del personaje activo
        self.animator = SpriteAnimator(
            sprite_path=sprite_path,
            total_frames=total_frames,
            frame_width=frame_width,
            frame_height=frame_height,
            columns=columns
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