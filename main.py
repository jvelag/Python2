# main.py
"""Entry point with main menu, save and victory"""

import pygame
import os
from game_manager import GameManager
from save_manager import save_game, load_game
from menu import show_main_menu, draw_pause_overlay, show_victory_screen
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Blue Prince - POO")
    clock = pygame.time.Clock()
    
    running = True
    
    while running:
        #  Display main menu
        menu_choice = show_main_menu(screen)
        
        if menu_choice == "quit":
            running = False
            break
        
        # Create new game or load
        gm = GameManager()
        
        if menu_choice == "load":
            success = load_game(gm.grid, gm.inventory, gm.player)
            if success:
                gm.message = "Partie chargée avec succès!"
            else:
                gm.message = "Aucune sauvegarde trouvée. Nouvelle partie."
        
        # Main game loop
        game_running = True
        paused = False
        victory = False
        game_over = False
        
        while game_running:
            # Obtain events
            events = pygame.event.get()
            
            # Manage global events first
            for event in events:
                if event.type == pygame.QUIT:
                    game_running = False
                    running = False
                
                elif event.type == pygame.KEYDOWN:

                    if victory or game_over:
                        if event.key == pygame.K_ESCAPE:
                            game_running = False  
                        elif event.key == pygame.K_r:

                            gm = GameManager()
                            victory = False
                            game_over = False
                            paused = False
                    
                    # Pause
                    elif event.key == pygame.K_p and not victory and not game_over:
                        paused = not paused  # Toggle pause
                    
                    # Save game (Ctrl+S)
                    elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if not victory and not game_over:
                            save_game(gm.grid, gm.inventory, gm.player)
                            gm.message = "Partie sauvegardée!"
                    

                    elif paused and event.key == pygame.K_ESCAPE:
                        game_running = False 
            

            if not paused and not victory and not game_over:

                gm.handle_events_from_main(events)
                gm.update()
                

                current_room = gm.grid.get_room(gm.player.row, gm.player.col)
                if current_room and current_room.room_type == "exit":
                    victory = True
                

                if gm.inventory.is_dead():
                    game_over = True
            
            gm.draw()
            
            if paused:
                draw_pause_overlay(screen)
            
            if victory:
                show_victory_screen(screen, gm.inventory)
            
            if game_over:
                show_game_over_screen(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    pygame.quit()


def show_game_over_screen(screen):
    """Muestra pantalla de Game Over"""
    font_large = pygame.font.SysFont("arial", 48, bold=True)
    font_small = pygame.font.SysFont("arial", 24)
    
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    title = font_large.render("GAME OVER", True, (255, 50, 50))
    subtitle = font_small.render("Vous n'avez plus de pas!", True, (255, 255, 255))
    hint1 = font_small.render("ESC - Retour au menu", True, (200, 200, 200))
    hint2 = font_small.render("R - Recommencer", True, (200, 200, 200))
    
    screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 200))
    screen.blit(subtitle, ((WINDOW_WIDTH - subtitle.get_width()) // 2, 270))
    screen.blit(hint1, ((WINDOW_WIDTH - hint1.get_width()) // 2, 340))
    screen.blit(hint2, ((WINDOW_WIDTH - hint2.get_width()) // 2, 380))


if __name__ == "__main__":
    main()


# ============================================================================
# STRUCTURE DES DOSSIERS DU PROJET
# ============================================================================
"""
blue_prince/
│
├── main.py                    
├── game_manager.py            
├── grid.py                    
├── player.py                  
├── inventory.py               
├── effects.py                 
├── ui.py                      
├── constants.py               
├── menu.py                    
├── save_manager.py            
├── item.py                    
├── room.py                    
├── door.py                    
├── rooms_catalog.py           
├── sound_manager.py           
│
├── assets/
│   ├── rooms/                 
│   │   ├── entry.png          
│   │   ├── sortie.png         
│   │   ├── bibliotheque.png   
│   │   ├── atelier.png        
│   │   ├── salle_tresor.png   
│   │   ├── piege.png          
│   │   ├── coffre.png         
│   │   ├── casiers.png        
│   │   ├── creuser.png        
│   │   ├── room_default.png   
│   │   ├── bedroom.png        
│   │   ├── corridor.png       
│   │   └── ...                
│   │
│   ├── icons/                 
│   │   ├── steps.png          
│   │   ├── gem.png            
│   │   ├── key.png            
│   │   ├── dice.png           
│   │   ├── gold.png           
│   │   ├── pelle.png          
│   │   ├── marteau.png        
│   │   ├── picklock.png       
│   │   ├── detecteur.png      
│   │   └── pattelapin.png     
│   │
│   ├── fonts/                 
│   │   └── OpenSans-Regular.ttf
│   │
│   └── audio/                 
│       ├── main_theme.mp3     
│       └── effects/           
│
└── saves/                     
    └── save.json              
"""