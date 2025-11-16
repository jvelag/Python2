import os
import random
import pygame

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOM_DIR = os.path.join(ROOT_DIR, "rooms")

# Colors
ROOM_COLORS = {
    "yellow": (255, 255, 100),    
    "green": (100, 255, 100),     
    "violet": (180, 100, 255),    
    "orange": (255, 165, 0),      
    "red": (255, 100, 100),       
    "blue": (100, 150, 255),      
    "neutral": (200, 200, 200),   
}

# ----------------------------
# Room
# ----------------------------
class Room:
    def __init__(self, name, image_name=None, room_type="normal", cost_gems=0,
                 effect_data=None, color_type="neutral", rarity=0):
        """
        :param name: nombre de la sala
        :param image_name: nombre archivo PNG
        :param room_type: "bibliotheque", "atelier", "tresor", "piege", "bedroom", etc.
        :param cost_gems: coste en gemas para elegir sala
        :param effect_data: diccionario con efectos (keys, gems, gold, food, etc.)
        :param color_type: "yellow", "green", "violet", "orange", "red", "blue", "neutral"
        :param rarity: 0 a 3 (0 más común, divide probabilidad por 3 cada nivel)
        """
        self.name = name
        self.image_name = image_name
        self.room_type = room_type
        self.cost_gems = cost_gems
        self.effect_data = effect_data if effect_data else {}
        self.color_type = color_type
        self.rarity = rarity

        self.image = None
        if image_name:
            full_path = os.path.join(ROOM_DIR, image_name)
            if os.path.exists(full_path):
                self.image = pygame.image.load(full_path).convert_alpha()

        # Asignar color según color_type
        self.color = ROOM_COLORS.get(color_type, ROOM_COLORS["neutral"])

    def get_probability_weight(self) -> float:
        """
        Calcula el peso de probabilidad según rareza.
        Cada nivel de rareza divide la probabilidad por 3.
        """
        return 1.0 / (3 ** self.rarity)
    
    def get_rarity_name(self) -> str:
        """Retorna el nombre de la rareza"""
        rarity_names = {
            0: "Commun",
            1: "Rare",
            2: "Épique",
            3: "Légendaire"
        }
        return rarity_names.get(self.rarity, f"Rareté {self.rarity}")

# ----------------------------
# Grid
# ----------------------------
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.discovered = [[False for _ in range(cols)] for _ in range(rows)]

        # Entree 
        self.start_pos = (rows - 1, 0)
        self.grid[rows - 1][0] = Room(
            "Entrée", 
            image_name="entry.png", 
            room_type="start", 
            color_type="blue",
            rarity=0
        )
        self.discovered[rows - 1][0] = True

        # Sortie 
        exit_r = 0
        exit_c = cols // 2
        self.exit_pos = (exit_r, exit_c)
        self.grid[exit_r][exit_c] = Room(
            "Antichambre", 
            image_name="sortie.png", 
            room_type="exit", 
            effect_data={"escape": True}, 
            color_type="blue",
            rarity=0
        )
        self.discovered[exit_r][exit_c] = True

    # Getters
    def get_room(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def is_discovered(self, r, c):
        return self.discovered[r][c]

    # Set room
    def set_room(self, r, c, room):
        """Coloca una room en la posición especificada"""
        if (r, c) == self.exit_pos:
            return False
        self.grid[r][c] = room
        self.discovered[r][c] = True
        return True

    def discover(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.discovered[r][c] = True

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols