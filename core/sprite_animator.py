from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRect

class SpriteAnimator:
    def __init__(self, sprite_path: str, total_frames: int, frame_width: int = 350, frame_height: int = 350, columns: int = 10):
        self.full_pixmap = QPixmap(sprite_path)
        self.total_frames = total_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.columns = columns
        self.current_frame = 0

        if self.full_pixmap.isNull():
            print(f"Error: No se pudo cargar el archivo de sprites: {sprite_path}")

    def get_next_frame(self) -> QPixmap:
        """Avanza al siguiente cuadro y devuelve la sub-imagen correspondiente."""
        if self.full_pixmap.isNull():
            return QPixmap()

        # Calcular fila y columna
        col = self.current_frame % self.columns
        row = self.current_frame // self.columns

        x = col * self.frame_width
        y = row * self.frame_height

        cropped = self.full_pixmap.copy(QRect(x, y, self.frame_width, self.frame_height))

        # Incrementar frame y reiniciar al llegar al límite de la animación
        self.current_frame = (self.current_frame + 1) % self.total_frames
        return cropped