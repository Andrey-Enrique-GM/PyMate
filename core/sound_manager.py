import os
import pygame



class SoundManager:
    def __init__(self, character_name: str, assets_dir: str = "assets"):
        self.character_name = character_name
        self.sounds_dir = os.path.join(assets_dir, "Sounds", character_name)
        
        # Inicializar el mezclador de pygame sin bloquear el sistema de audio
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.sounds = {}
        self.load_sounds()


    def load_sounds(self):
        """ Escanea la carpeta del personaje y carga todos los archivos .wav """
        if not os.path.exists(self.sounds_dir):
            print(f"[SoundManager] Error: No se encontró la carpeta {self.sounds_dir}")
            return

        for file_name in os.listdir(self.sounds_dir):
            if file_name.lower().endswith(".wav"):
                action_name = os.path.splitext(file_name)[0].lower()
                full_path = os.path.join(self.sounds_dir, file_name)
                try:
                    self.sounds[action_name] = pygame.mixer.Sound(full_path)
                except Exception as e:
                    print(f"[SoundManager] Error al cargar {full_path}: {e}")


    def play_sound(self, sound_name: str):
        """ Reproduce el sonido de una acción si existe """
        sound_key = sound_name.lower()
        if sound_key in self.sounds:
            self.sounds[sound_key].play()
