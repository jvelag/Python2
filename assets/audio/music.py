import pygame

""" 
Definition d'une class pour la gestion des effets audio
"""

class AudioManager:
    """
    Fichiers:

    - main_theme: loop de musique pendant tous le jeu
    - door_open: bruit overture d'une porte 
    - door_locked: bruit porte verrouillée
    - pick_item: ajout d'un nouvel objet
    - game_over: fin du jeu
    """

    def __init__(self):
        pygame.mixer.music.load("assets/music/main_theme.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.door_open = pygame.mixer.Sound("assets/sfx/door_open.wav")
        self.door_locked = pygame.mixer.Sound("assets/sfx/door_locked.wav")
        self.pick_item = pygame.mixer.Sound("assets/sfx/pick_item.wav")
        self.game_over = pygame.mixer.Sound("assets/sfx/game_over.wav")