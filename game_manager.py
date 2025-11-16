# game_manager.py
"""GameManager: orchestrates the game, events, update and draw calls."""

import os
import random
import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_ROWS, GRID_COLS,
    FONT_DIR, AUDIO_DIR, FPS,
    BLACK, WHITE, CURSOR_COLOR
)
from grid import Grid, Room
from player import Player
from inventory import Inventory
from ui import draw_grid, draw_inventory, draw_message
from effects import apply_room_effect


class GameManager:
    """Main game class (GameManager)."""

    def __init__(self, width: int | None = None, height: int | None = None):
        pygame.init()
        pygame.display.set_caption("Blue Prince - POO")

        if width is None:
            width = WINDOW_WIDTH
        if height is None:
            height = WINDOW_HEIGHT

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Core model
        self.grid = Grid(rows=GRID_ROWS, cols=GRID_COLS)
        self.inventory = Inventory()

        # Player starts at the entrance (bottom-left)
        start_r = self.grid.rows - 1
        start_c = 0
        self.player = Player(start_row=start_r, start_col=start_c, inventory=self.inventory)
        self.grid.discover(start_r, start_c)

        # UI / fonts
        font_path = os.path.join(FONT_DIR, "OpenSans-Regular.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 16)
            self.large_font = pygame.font.Font(font_path, 20)
        else:
            self.font = pygame.font.SysFont("arial", 16)
            self.large_font = pygame.font.SysFont("arial", 20, bold=True)

        # Audio
        try:
            pygame.mixer.init()
            music_path_mp3 = os.path.join(AUDIO_DIR, "main_theme.mp3")
            music_path_wav = os.path.join(AUDIO_DIR, "main_theme.wav")
            if os.path.exists(music_path_mp3):
                pygame.mixer.music.load(music_path_mp3)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            elif os.path.exists(music_path_wav):
                pygame.mixer.music.load(music_path_wav)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
        except Exception:
            pass  # audio not critical

        # State
        self.message = "ZQSD pour deplacer le curseur. Espace pour entrer."
        self.in_modal = False
        self.modal_options: list[Room] = []
        self.selected_choice_idx = 0
        self.modal_target_pos: tuple | None = None

    # --------------------
    # Event handling
    # --------------------
    def handle_events_from_main(self, events):
        """
        Maneja eventos pasados desde main.py
        Procesa movimiento del cursor y acciones del jugador
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Modal open?
                if self.in_modal:
                    self._handle_modal_key(event.key)
                    continue

                # Cursor movement - ZQSD
                if event.key == pygame.K_z:
                    self.player.move_cursor(-1, 0, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved UP to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_s:
                    self.player.move_cursor(1, 0, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved DOWN to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_q:
                    self.player.move_cursor(0, -1, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved LEFT to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_d:
                    self.player.move_cursor(0, 1, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved RIGHT to ({self.player.sel_row}, {self.player.sel_col})")
                
                # Arrow keys
                elif event.key == pygame.K_UP:
                    self.player.move_cursor(-1, 0, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved UP to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_DOWN:
                    self.player.move_cursor(1, 0, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved DOWN to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_LEFT:
                    self.player.move_cursor(0, -1, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved LEFT to ({self.player.sel_row}, {self.player.sel_col})")
                elif event.key == pygame.K_RIGHT:
                    self.player.move_cursor(0, 1, self.grid.rows, self.grid.cols)
                    print(f"DEBUG: Cursor moved RIGHT to ({self.player.sel_row}, {self.player.sel_col})")

                elif event.key == pygame.K_SPACE:
                    print(f"DEBUG: SPACE pressed at cursor ({self.player.sel_row}, {self.player.sel_col})")
                    sr, sc = self.player.sel_row, self.player.sel_col
                    if self.player.can_move_to(sr, sc):
                        if self.grid.is_discovered(sr, sc):
                            self.player.move_to(sr, sc)
                            room = self.grid.get_room(sr, sc)
                            effect_msg = apply_room_effect(room, self.player, self.inventory, self.grid)
                            self.message = f"{effect_msg} | Pas restants: {self.inventory.steps}"
                            if room.room_type == "exit":
                                self.message = "You Win! Appuyez sur ESC pour quitter."
                                self.running = False
                        else:
                            self.open_door_modal(sr, sc)
                    else:
                        self.message = "La destination doit être adjacente au joueur."

                elif event.key == pygame.K_RETURN:
                    self.player.reset_cursor_to_player()
                    self.message = "Curseur recentré."
                    print(f"DEBUG: Cursor reset to player position ({self.player.row}, {self.player.col})")

    def handle_events(self):
        """Método original - NO USAR, solo para compatibilidad"""
        pass

    # --------------------
    # Modal handling
    # --------------------
    def _handle_modal_key(self, key):
        """Handle key presses when modal is open"""
        if key in (pygame.K_q, pygame.K_LEFT):
            self.selected_choice_idx = max(0, self.selected_choice_idx - 1)
        elif key in (pygame.K_d, pygame.K_RIGHT):
            self.selected_choice_idx = min(len(self.modal_options) - 1, self.selected_choice_idx + 1)
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            if not self.modal_options or self.modal_target_pos is None:
                self.in_modal = False
                return

            choice = self.modal_options[self.selected_choice_idx]
            
            # Check if room requires key to enter
            if choice.effect_data.get("requires_key_to_enter", False):
                if self.inventory.keys > 0:
                    self.inventory.keys -= 1
                    self.message = f"Vous utilisez une clé pour entrer dans {choice.name}."
                else:
                    self.message = f"Vous avez besoin d'une clé pour entrer dans {choice.name}."
                    return
            
            # Check gem cost
            cost = choice.cost_gems
            if cost > 0:
                ok = self.inventory.use_gems(cost)
                if not ok:
                    self.message = f"Pas assez de gemmes pour choisir {choice.name}."
                    return

            tr, tc = self.modal_target_pos
            self.grid.set_room(tr, tc, choice)
            self.player.move_to(tr, tc)
            effect_msg = apply_room_effect(choice, self.player, self.inventory, self.grid)

            self.in_modal = False
            self.modal_options = []
            self.selected_choice_idx = 0
            self.modal_target_pos = None
            self.message = f"{effect_msg} | Pas restants: {self.inventory.steps}"

        elif key == pygame.K_ESCAPE:
            self.in_modal = False
            self.modal_options = []
            self.message = "Choix annulé."

    # --------------------
    # Door / room generation
    # --------------------
    def open_door_modal(self, r: int, c: int):
        """
        Opens modal to choose from 3 randomly drawn rooms.
        Only includes actual ROOMS, not items (items are inside rooms).
        """
        # Catalog of actual ROOMS (not items/objects)
        candidate_rooms = [
            # Blue rooms (common, neutral)
            Room("Couloir", image_name="Couloir.png", room_type="neutral", 
                 cost_gems=0, color_type="blue", rarity=0),
            Room("Salle Vide", image_name="room_default.png", room_type="neutral", 
                 cost_gems=0, color_type="blue", rarity=0),
            
            # Green rooms (gardens - contain permanent items or dig spots)
            Room("Bibliothèque", image_name="bibliotheque.png", room_type="bibliotheque", 
                 cost_gems=1, color_type="green", rarity=1, 
                 effect_data={"gems": 1}),
            Room("Veranda", image_name="Veranda.png", room_type="veranda", 
                 cost_gems=2, color_type="green", rarity=2,
                 effect_data={"boost_green": True}),
            
            # Yellow rooms (workshops - contain keys)
            Room("Atelier", image_name="atelier.png", room_type="atelier", 
                 cost_gems=1, color_type="yellow", rarity=1,
                 effect_data={"keys": 1}),
            
            # Violet rooms (bedrooms - contain food)
            Room("Chambre", image_name="Chambre.png", room_type="bedroom", 
                 cost_gems=1, color_type="violet", rarity=1,
                 effect_data={"has_food": True}),
            
            # Orange rooms (corridors - many doors)
            Room("Grand Couloir", image_name="room_default.png", room_type="corridor", 
                 cost_gems=0, color_type="orange", rarity=0),
            
            # Red rooms (dangerous - traps)
            Room("Salle Piégée", image_name="piege.png", room_type="piege", 
                 cost_gems=0, color_type="red", rarity=1,
                 effect_data={"trap_damage": 5}),
            
            # Special rooms with containers
            Room("Salle Trésor", image_name="salle_tresor.png", room_type="tresor", 
                 cost_gems=2, color_type="yellow", rarity=2,
                 effect_data={"gold": 5}),
            Room("Salle aux Coffres", image_name="coffre.png", room_type="coffre", 
                 cost_gems=1, color_type="blue", rarity=1,
                 effect_data={"chest_count": 1, "requires_key": True}),
            Room("Vestiaire", image_name="casiers.png", room_type="casier", 
                 cost_gems=1, color_type="blue", rarity=1,
                 effect_data={"locker_count": 2, "requires_key": True}),
            Room("Jardin", image_name="Jardin.png", room_type="creuser", 
                 cost_gems=1, color_type="green", rarity=1,
                 effect_data={"dig_spots": 1, "requires_shovel": True}),
            
            # Locked room (requires key to enter)
            Room("Coffre-Fort", image_name="coffre.png", room_type="locked_room",
                 cost_gems=2, color_type="yellow", rarity=2,
                 effect_data={"gold": 10, "gems": 2, "requires_key_to_enter": True}),
        ]

        # Filter out exit room
        candidate_rooms = [rm for rm in candidate_rooms if rm.room_type != "exit"]

        # Select 3 rooms
        if len(candidate_rooms) <= 3:
            choices = candidate_rooms[:]
        else:
            # Draw according to rarity weights
            weights = [rm.get_probability_weight() for rm in candidate_rooms]
            choices = random.choices(candidate_rooms, weights=weights, k=3)

        # Ensure at least one free room (cost_gems == 0)
        if not any(rm.cost_gems == 0 for rm in choices):
            free_rooms = [rm for rm in candidate_rooms if rm.cost_gems == 0]
            if free_rooms:
                choices[0] = random.choice(free_rooms)

        self.in_modal = True
        self.modal_options = choices
        self.modal_target_pos = (r, c)
        self.selected_choice_idx = 0
        self.message = "Choisissez une salle avec Q/D et validez avec Entrée."

    # --------------------
    # Update / Draw / Loop
    # --------------------
    def update(self):
        if self.inventory.is_dead():
            self.message = "Vous n'avez plus de pas. Partie terminée. Appuyez sur ESC."
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        draw_grid(self.screen, self.grid, (self.player.row, self.player.col),
                  (self.player.sel_row, self.player.sel_col))
        draw_inventory(self.screen, self.inventory, self.font)
        draw_message(self.screen, self.font, self.message)
        if self.in_modal and self.modal_options:
            self._draw_modal()

    def _draw_modal(self):
        """Draw modal with room name, color, and cost"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        w, h = 620, 280
        x = (WINDOW_WIDTH - w) // 2
        y = (WINDOW_HEIGHT - h) // 2
        pygame.draw.rect(self.screen, WHITE, (x, y, w, h))
        pygame.draw.rect(self.screen, BLACK, (x, y, w, h), 3)

        # Title
        title_txt = self.large_font.render("Choisissez une salle:", True, BLACK)
        self.screen.blit(title_txt, (x + 20, y + 15))

        spacing = 20
        box_w = (w - 4 * spacing) // 3
        box_h = h - 100
        bx = x + spacing
        by = y + 60

        for idx, room in enumerate(self.modal_options):
            rect = pygame.Rect(bx + idx * (box_w + spacing), by, box_w, box_h)
            
            # Background with room color
            pygame.draw.rect(self.screen, room.color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Room name
            name_txt = self.font.render(room.name, True, BLACK)
            self.screen.blit(name_txt, (rect.x + 6, rect.y + 6))
            
            # Color type
            color_txt = self.font.render(f"({room.color_type})", True, BLACK)
            self.screen.blit(color_txt, (rect.x + 6, rect.y + 26))
            
            # Gem cost
            cost_txt = self.font.render(f"Cout: {room.cost_gems} gemmes", True, BLACK)
            self.screen.blit(cost_txt, (rect.x + 6, rect.y + 46))
            
            # Rarity
            rarity_txt = self.font.render(f"Rarete: {room.rarity}/3", True, BLACK)
            self.screen.blit(rarity_txt, (rect.x + 6, rect.y + 66))
            
            # Key requirement indicator
            if room.effect_data.get("requires_key_to_enter", False):
                key_txt = self.font.render("Cle requise!", True, (200, 0, 0))
                self.screen.blit(key_txt, (rect.x + 6, rect.y + 86))
            
            # Highlight if selected
            if idx == self.selected_choice_idx:
                pygame.draw.rect(self.screen, CURSOR_COLOR, rect, 5)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()