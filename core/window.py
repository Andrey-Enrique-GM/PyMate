import math
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QCursor
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
        self.setMouseTracking(True)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.label = QLabel(self)
        self.label.setFixedSize(self.target_size, self.target_size)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)

        self.resize(self.target_size, self.target_size)

        # Animador IDLE permanente
        idle_data = self.character.get_animation_data("idle")
        self.idle_animator = SpriteAnimator(
            sprite_path=idle_data["path"],
            total_frames=idle_data["total_frames"],
            frame_width=idle_data["frame_width"],
            frame_height=idle_data["frame_height"],
            columns=idle_data["columns"]
        )

        # Animador para acciones secundarias
        self.action_animator = None

        # Temporizador de renderizado de animación
        interval_ms = int(1000 / fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(interval_ms)

        # Configuración de movimiento
        self.is_following = False
        self.follow_timer = QTimer(self)
        self.follow_timer.timeout.connect(self.follow_cursor)
        
        # Parámetros de velocidad constante y radio de detención
        self.speed = 5  # Píxeles por paso
        self.follow_radius = 120.0  # Radio para detenerse antes de tocar el cursor

        self.is_dragging = False
        self.drag_offset = QPoint()


    def set_state(self, new_state: str):
        if self.current_state == new_state:
            return
            
        self.current_state = new_state.lower()

        if self.current_state == "idle":
            self.action_animator = None
        else:
            anim_data = self.character.get_animation_data(self.current_state)
            self.action_animator = SpriteAnimator(
                sprite_path=anim_data["path"],
                total_frames=anim_data["total_frames"],
                frame_width=anim_data["frame_width"],
                frame_height=anim_data["frame_height"],
                columns=anim_data["columns"]
            )


    def update_animation(self):
        if self.current_state == "idle":
            pixmap = self.idle_animator.get_next_frame()
        else:
            pixmap = self.action_animator.get_next_frame()
            
            if self.current_state == "click":
                if self.action_animator.current_frame == 0:
                    if self.underMouse():
                        self.set_state("hover")
                    else:
                        self.set_state("idle")
                    return

        if not pixmap.isNull():
            self.label.setPixmap(pixmap)


    def follow_cursor(self):
        """Mueve a la mascota hacia el cursor a velocidad constante hasta alcanzar el radio."""
        if not self.is_following:
            return

        cursor_pos = QCursor.pos()
        center_pos = self.geometry().center()

        # Distancia entre el centro de la mascota y el cursor
        dx = cursor_pos.x() - center_pos.x()
        dy = cursor_pos.y() - center_pos.y()
        distance = math.hypot(dx, dy)

        # Si está fuera del radio permitido, camina hacia el cursor
        if distance > self.follow_radius:
            step_x = (dx / distance) * self.speed
            step_y = (dy / distance) * self.speed

            new_x = int(self.x() + step_x)
            new_y = int(self.y() + step_y)

            self.move(new_x, new_y)


    def enterEvent(self, event):
        if not self.is_dragging and self.current_state != "click" and not self.is_following:
            self.set_state("hover")
        super().enterEvent(event)


    def leaveEvent(self, event):
        if not self.is_dragging and self.current_state != "click" and not self.is_following:
            self.set_state("idle")
        super().leaveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_following = not self.is_following
            
            if self.is_following:
                self.follow_timer.start(16)
                self.set_state("idle")
            else:
                self.follow_timer.stop()
                if self.underMouse():
                    self.set_state("hover")
                else:
                    self.set_state("idle")
                    
            event.accept()
            
        elif event.button() == Qt.MouseButton.RightButton:
            self.set_state("click")
            event.accept()


    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton and not self.is_following:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            event.accept()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            event.accept()
            
        elif event.button() == Qt.MouseButton.RightButton:
            event.accept()
