from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRect



class SpriteAnimator:
    def __init__(self, sprite_path: str, total_frames: int = 340, frame_width: int = 350, frame_height: int = 350, columns: int = 10):
        self.load_anim(sprite_path, total_frames, frame_width, frame_height, columns)


    def load_anim(self, sprite_path: str, total_frames: int, frame_width: int, frame_height: int, columns: int):
        self.full_pixmap = QPixmap(sprite_path)
        self.total_frames = total_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.columns = columns
        self.current_frame = 0

        if self.full_pixmap.isNull():
            print(f"Error cargando: {sprite_path}")


    def get_next_frame(self) -> QPixmap:
        if self.full_pixmap.isNull():
            return QPixmap()

        col = self.current_frame % self.columns
        row = self.current_frame // self.columns

        x = col * self.frame_width
        y = row * self.frame_height

        cropped = self.full_pixmap.copy(QRect(x, y, self.frame_width, self.frame_height))

        self.current_frame = (self.current_frame + 1) % self.total_frames
        return cropped
        