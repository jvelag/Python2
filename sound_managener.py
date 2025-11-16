
# Mohand
# sound_manager.py
"""
 - assets/sounds/music/<name>.mp3 (o .ogg)
 - assets/sounds/effects/<name>.wav
"""

import os
import pygame

MUSIC_DIR = os.path.join("assets", "sounds", "music")
EFFECTS_DIR = os.path.join("assets", "sounds", "effects")

def init_sound():
    try:
        pygame.mixer.init()
    except Exception as e:
        print("Audio init failed:", e)

def play_music(filename: str, loop: bool = True):
    path = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(path):
        print("Music file not found:", path)
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1 if loop else 0)
    except Exception as e:
        print("Error playing music:", e)

def stop_music():
    pygame.mixer.music.stop()

def play_effect(filename: str):
    path = os.path.join(EFFECTS_DIR, filename)
    if not os.path.exists(path):
        print("Effect file not found:", path)
        return
    try:
        s = pygame.mixer.Sound(path)
        s.play()
    except Exception as e:
        print("Error playing effect:", e)
