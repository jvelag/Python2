# ui.py
"""Rendering utilities: draw grid, player, inventory panel and simple modal for 'tirage'."""

import pygame
import os
from typing import Tuple
from constants import *
from grid import Grid, Room

FONT_SIZE = 18

def draw_grid(surface: pygame.Surface, grid: Grid, player_pos: Tuple[int,int], cursor_pos: Tuple[int,int]):
    """Dessine la grille et les salles."""
    area_w = GRID_AREA_WIDTH
    area_h = GRID_AREA_HEIGHT
    cell_w = area_w // grid.cols
    cell_h = area_h // grid.rows

    # Background
    grid_rect = pygame.Rect(0, 0, area_w, area_h)
    pygame.draw.rect(surface, DARK_GRAY, grid_rect)

    # Draw cells
    for r in range(grid.rows):
        for c in range(grid.cols):
            x = c * cell_w
            y = r * cell_h
            cell_rect = pygame.Rect(x, y, cell_w, cell_h)
            room = grid.get_room(r, c)
            if room is None:
                pygame.draw.rect(surface, UNKNOWN_ROOM_COLOR, cell_rect)
            else:
                if hasattr(room, "image") and room.image:
                    img = pygame.transform.scale(room.image, (cell_w, cell_h))
                    surface.blit(img, (x, y))
                else:
                    pygame.draw.rect(surface, room.color, cell_rect)
            pygame.draw.rect(surface, GRID_LINE_COLOR, cell_rect, 1)

    # Player highlight
    pr, pc = player_pos
    prow = pygame.Rect(pc * cell_w, pr * cell_h, cell_w, cell_h)
    pygame.draw.rect(surface, BLUE, prow, 4)

    # Cursor highlight
    cr, cc = cursor_pos
    crect = pygame.Rect(cc * cell_w, cr * cell_h, cell_w, cell_h)
    pygame.draw.rect(surface, CURSOR_COLOR, crect, 3)


def draw_inventory(surface: pygame.Surface, inventory, font: pygame.font.Font):
    """Dessine le panneau d'inventaire avec icônes."""
    x0 = GRID_AREA_WIDTH
    panel = pygame.Rect(x0, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, GRAY, panel)

    margin = 12
    y = margin
    title_s = font.render("INVENTAIRE", True, BLACK)
    surface.blit(title_s, (x0 + margin, y))
    y += 30

    # Consumables
    consumables = [
        ("Pas", inventory.steps, "steps.png"),
        ("Gemmes", inventory.gems, "gem.png"),
        ("Clés", inventory.keys, "key.png"),
        ("Dés", inventory.dice, "dice.png"),
        ("Pièces", inventory.gold, "gold.png"),
    ]
    icon_size = 24
    for name, count, icon_file in consumables:
        icon_path = os.path.join(ICON_DIR, icon_file)
        if os.path.exists(icon_path):
            icon_img = pygame.image.load(icon_path).convert_alpha()
            icon_img = pygame.transform.scale(icon_img, (icon_size, icon_size))
            surface.blit(icon_img, (x0 + margin, y))
        s = font.render(f"{name}: {count}", True, BLACK)
        surface.blit(s, (x0 + margin + icon_size + 6, y + 2))
        y += icon_size + 6

    y += 8
    perm_title = font.render("Objets permanents:", True, BLACK)
    surface.blit(perm_title, (x0 + margin, y))
    y += 22

    permanents = [
        ("Pelle", inventory.shovel, "pelle.png"),
        ("Marteau", inventory.hammer, "marteau.png"),
        ("Kit crochetage", inventory.picklock_kit, "picklock.png"),
        ("Detecteur", inventory.metal_detector, "detecteur.png"),
        ("Patte lapin", inventory.rabbit_foot, "pattelapin.png"),
    ]
    for name, have, icon_file in permanents:
        icon_path = os.path.join(ICON_DIR, icon_file)
        if os.path.exists(icon_path):
            icon_img = pygame.image.load(icon_path).convert_alpha()
            icon_img = pygame.transform.scale(icon_img, (icon_size, icon_size))
            surface.blit(icon_img, (x0 + margin, y))
        else:
            pygame.draw.rect(surface, DARK_GRAY, (x0 + margin, y, icon_size, icon_size))
            print(f"Icon not found: {icon_path}")
        s = font.render(f"{name}: {'✓' if have else 'x'}", True, BLACK)
        surface.blit(s, (x0 + margin + icon_size + 6, y + 2))
        y += icon_size + 6


def draw_message(surface: pygame.Surface, font: pygame.font.Font, message: str):
    """Petit texte en bas center."""
    s = font.render(message, True, WHITE)
    rect = s.get_rect(center=(GRID_AREA_WIDTH // 2, WINDOW_HEIGHT - 20))
    surface.blit(s, rect)