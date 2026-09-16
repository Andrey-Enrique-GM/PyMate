from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from core.sprite_animator import SpriteAnimator
from core.character import Character



class PetWindow(QWidget):
    def __init__(self, character: Character, target_size: int = 230, fps: int = 35):
        super().__init__()

        self.character = character
        self.target_size = target_size
        self.current_state = "idle"

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

        # Cargar estado inicial
        anim_data = self.character.get_animation_data(self.current_state)
        self.animator = SpriteAnimator(
            sprite_path=anim_data["path"],
            total_frames=anim_data["total_frames"],
            frame_width=anim_data["frame_width"],
            frame_height=anim_data["frame_height"],
            columns=anim_data["columns"]
        )

        interval_ms = int(1000 / fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(interval_ms)

        self.is_dragging = False
        self.drag_offset = QPoint()


    def set_state(self, new_state: str):
        if self.current_state == new_state:
            return
        self.current_state = new_state
        anim_data = self.character.get_animation_data(new_state)
        self.animator.load_anim(
            sprite_path=anim_data["path"],
            total_frames=anim_data["total_frames"],
            frame_width=anim_data["frame_width"],
            frame_height=anim_data["frame_height"],
            columns=anim_data["columns"]
        )


    def update_animation(self):
        pixmap = self.animator.get_next_frame()
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.set_state("grab")  # Cambia a estado agarre
            event.accept()


    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            event.accept()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.set_state("idle")  # Vuelve a idle
            event.accept()
