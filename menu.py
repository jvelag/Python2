# menu.py


import pygame
from typing import Tuple
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

FONT_NAME = None  

def show_main_menu(screen: pygame.Surface) -> str:
    """
    Muestra un menú simple. Devuelve 'new', 'load' o 'quit'.
    Bloqueante - espera la selección del usuario.
    """
    clock = pygame.time.Clock()
    w, h = screen.get_size()
    font = pygame.font.SysFont("arial", 32, bold=True)
    small = pygame.font.SysFont("arial", 20)
    tiny = pygame.font.SysFont("arial", 16)
    
    selected = 0
    options = ["Nouvelle Partie", "Charger Partie", "Quitter"]
    running = True
    
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quit"
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_z):
                    selected = (selected - 1) % len(options)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    if options[selected] == "Nouvelle Partie":
                        return "new"
                    elif options[selected] == "Charger Partie":
                        return "load"
                    elif options[selected] == "Quitter":
                        return "quit"
        

        screen.fill((10, 10, 30))
        
        title = font.render(" BLUE PRINCE", True, (150, 200, 255))
        screen.blit(title, ((w - title.get_width()) // 2, 80))
        
        subtitle = tiny.render("Projet POO 2025", True, (180, 180, 180))
        screen.blit(subtitle, ((w - subtitle.get_width()) // 2, 130))
        
        for i, opt in enumerate(options):
            if i == selected:
                color = (255, 255, 100)
                prefix = "▶ "
            else:
                color = (200, 200, 200)
                prefix = "  "
            
            txt = small.render(prefix + opt, True, color)
            screen.blit(txt, ((w - txt.get_width()) // 2, 220 + i * 50))
        
        hint1 = tiny.render("↑↓ ou Z/S pour naviguer", True, (150, 150, 150))
        hint2 = tiny.render("Entrée pour sélectionner", True, (150, 150, 150))
        screen.blit(hint1, ((w - hint1.get_width()) // 2, h - 80))
        screen.blit(hint2, ((w - hint2.get_width()) // 2, h - 55))
        

        save_hint = tiny.render("Ctrl+S pour sauvegarder pendant le jeu", True, (100, 150, 100))
        screen.blit(save_hint, ((w - save_hint.get_width()) // 2, h - 25))
        
        pygame.display.flip()
        clock.tick(30)


def draw_pause_overlay(screen: pygame.Surface):
    """Dibuja overlay de pausa (no bloqueante)."""
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont("arial", 36, bold=True)
    font_small = pygame.font.SysFont("arial", 20)
    
    title = font_large.render("⏸  PAUSE", True, (255, 255, 255))
    screen.blit(title, ((w - title.get_width()) // 2, h // 2 - 60))
    
    hint1 = font_small.render("P - Reprendre", True, (200, 200, 200))
    hint2 = font_small.render("Ctrl+S - Sauvegarder", True, (200, 200, 200))
    hint3 = font_small.render("ESC - Quitter au menu", True, (200, 200, 200))
    
    screen.blit(hint1, ((w - hint1.get_width()) // 2, h // 2))
    screen.blit(hint2, ((w - hint2.get_width()) // 2, h // 2 + 35))
    screen.blit(hint3, ((w - hint3.get_width()) // 2, h // 2 + 70))


def show_victory_screen(screen: pygame.Surface, inventory):
    """
    Écran de victoire lorsque vous atteignez la ligne d'arrivée.
    Affiche les statistiques finales.
    """
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_huge = pygame.font.SysFont("arial", 56, bold=True)
    font_large = pygame.font.SysFont("arial", 28, bold=True)
    font_medium = pygame.font.SysFont("arial", 22)
    font_small = pygame.font.SysFont("arial", 18)
    
    title = font_huge.render(" VICTOIRE! ", True, (255, 215, 0))
    screen.blit(title, ((w - title.get_width()) // 2, 60))
    
    subtitle = font_large.render("Vous avez atteint l'Antichambre!", True, (200, 255, 200))
    screen.blit(subtitle, ((w - subtitle.get_width()) // 2, 130))
    
    stats_y = 200
    stats_title = font_medium.render(" Statistiques finales:", True, (255, 255, 255))
    screen.blit(stats_title, ((w - stats_title.get_width()) // 2, stats_y))
    
    stats = [
        f"Pas restants: {inventory.steps}",
        f"Pièces d'or: {inventory.gold}",
        f"Gemmes: {inventory.gems}",
        f"Clés: {inventory.keys}",
        f"Dés: {inventory.dice}",
    ]
    
    stats_y += 50
    for stat in stats:
        txt = font_small.render(stat, True, (220, 220, 220))
        screen.blit(txt, ((w - txt.get_width()) // 2, stats_y))
        stats_y += 30
    
    perms_y = stats_y + 20
    perms_title = font_medium.render(" Objets obtenus:", True, (255, 255, 255))
    screen.blit(perms_title, ((w - perms_title.get_width()) // 2, perms_y))
    
    perms = []
    if inventory.shovel:
        perms.append("Pelle ")
    if inventory.hammer:
        perms.append("Marteau ")
    if inventory.picklock_kit:
        perms.append("Kit de crochetage ")
    if inventory.metal_detector:
        perms.append("Détecteur de métaux ")
    if inventory.rabbit_foot:
        perms.append("Patte de lapin ")
    
    if perms:
        perms_y += 40
        for perm in perms:
            txt = font_small.render(perm, True, (150, 255, 150))
            screen.blit(txt, ((w - txt.get_width()) // 2, perms_y))
            perms_y += 28
    else:
        perms_y += 40
        txt = font_small.render("Aucun objet permanent", True, (180, 180, 180))
        screen.blit(txt, ((w - txt.get_width()) // 2, perms_y))
    
    hint_y = h - 80
    hint1 = font_medium.render("ESC - Retour au menu", True, (200, 200, 200))
    hint2 = font_medium.render("R - Rejouer", True, (200, 200, 200))
    
    screen.blit(hint1, ((w - hint1.get_width()) // 2, hint_y))
    screen.blit(hint2, ((w - hint2.get_width()) // 2, hint_y + 35))


def show_game_over_screen(screen: pygame.Surface):
    """Pantalla de derrota"""
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_huge = pygame.font.SysFont("arial", 56, bold=True)
    font_large = pygame.font.SysFont("arial", 28)
    font_medium = pygame.font.SysFont("arial", 22)
    
    title = font_huge.render(" GAME OVER ", True, (255, 80, 80))
    screen.blit(title, ((w - title.get_width()) // 2, 180))
    
    subtitle = font_large.render("Vous n'avez plus de pas!", True, (255, 255, 255))
    screen.blit(subtitle, ((w - subtitle.get_width()) // 2, 260))
    
    hint1 = font_medium.render("ESC - Retour au menu", True, (200, 200, 200))
    hint2 = font_medium.render("R - Recommencer", True, (200, 200, 200))
    
    screen.blit(hint1, ((w - hint1.get_width()) // 2, 350))
    screen.blit(hint2, ((w - hint2.get_width()) // 2, 390))