import pygame
import random

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_file = f"Sounds/Musics/music{random.randint(1, 11)}.mp3"

    def play_music(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

    def play_spawn(self):
        effect_file = f"Sounds/Spawn/spawn{random.randint(1, 5)}.mp3"
        sound = pygame.mixer.Sound(effect_file)
        sound.set_volume(0.15)
        sound.play()

    def play_validation(self):
        effect_file = f"Sounds/validation.mp3"
        sound = pygame.mixer.Sound(effect_file)
        sound.set_volume(0.2)
        sound.play()