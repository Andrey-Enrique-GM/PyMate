import math
import random
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtGui import QGuiApplication



class AutoWalker(QObject):
    def __init__(self, window, min_rest_sec: int = 20, max_rest_sec: int = 40, walk_duration_sec: float = 3.5, speed: float = 0.5):
        super().__init__()
        self.window = window
        self.min_rest = min_rest_sec
        self.max_rest = max_rest_sec
        self.walk_duration_ms = int(walk_duration_sec * 1000)
        
        # Velocidad en píxeles por paso (modificable en window.py)
        self.speed = speed

        # Temporizadores
        self.rest_timer = QTimer(self)
        self.rest_timer.setSingleShot(True)
        self.rest_timer.timeout.connect(self.start_walk)

        self.walk_timer = QTimer(self)
        self.walk_timer.timeout.connect(self._step)

        self.duration_timer = QTimer(self)
        self.duration_timer.setSingleShot(True)
        self.duration_timer.timeout.connect(self.stop_walk)

        self.dx = 0.0
        self.dy = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.is_walking = False


    def get_walk_direction(self, dx: float, dy: float) -> str:
        """ Determina la animación de caminata según el ángulo de dirección en 4 ejes """
        angle = math.degrees(math.atan2(dy, dx))

        if -45 <= angle < 45:
            return "walkright"
        elif 45 <= angle < 135:
            return "walkdown"
        elif angle >= 135 or angle < -135:
            return "walkleft"
        else:
            return "walkup"


    def schedule_next_walk(self):
        """ Programa el próximo paseo con un intervalo de descanso aleatorio """
        if not self.is_walking:
            wait_time_ms = random.randint(self.min_rest * 1000, self.max_rest * 1000)
            self.rest_timer.start(wait_time_ms)


    def start_walk(self):
        """ Calcula una dirección aleatoria, asigna la animación y comienza a caminar """
        if self.window.current_state != "idle" or self.window.is_following or self.window.is_dragging:
            self.schedule_next_walk()
            return

        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        # Posición flotante actual
        self.pos_x = float(self.window.x())
        self.pos_y = float(self.window.y())

        # Validar límites de pantalla
        screen_geo = QGuiApplication.primaryScreen().geometry()
        future_x = self.pos_x + (self.dx * (self.walk_duration_ms / 16))
        future_y = self.pos_y + (self.dy * (self.walk_duration_ms / 16))

        if future_x < 0 or future_x + self.window.width() > screen_geo.width():
            self.dx *= -1
        if future_y < 0 or future_y + self.window.height() > screen_geo.height():
            self.dy *= -1

        # Asignar la animación de caminata según la dirección calculada
        walk_state = self.get_walk_direction(self.dx, self.dy)
        self.window.set_state(walk_state)

        self.is_walking = True
        self.walk_timer.start(16)
        self.duration_timer.start(self.walk_duration_ms)


    def _step(self):
        """ Aplica un paso de movimiento """
        if not self.is_walking:
            return

        if self.window.is_dragging or self.window.is_following or self.window.current_state in ["intro", "outro", "grab", "click"]:
            self.stop_walk()
            return

        self.pos_x += self.dx
        self.pos_y += self.dy
        self.window.move(int(self.pos_x), int(self.pos_y))


    def stop_walk(self):
        """ Detiene el movimiento y restablece el descanso (idle) """
        self.is_walking = False
        self.walk_timer.stop()
        self.duration_timer.stop()

        if self.window.current_state not in ["intro", "outro", "grab", "click"] and not self.window.is_following:
            self.window.set_state("idle")

        self.schedule_next_walk()


    def cancel(self):
        """ Cancela temporizadores """
        self.is_walking = False
        self.rest_timer.stop()
        self.walk_timer.stop()
        self.duration_timer.stop()
