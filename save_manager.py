# save_manager.py - MEJORADO
"""
HOW SAVING WORKS:
==========================
1. Press Ctrl+S during gameplay.
2. The entire state (grid, inventory, player) is serialised to JSON.
3. It is saved in: saves/save.json

WHAT IS SAVED:
==============
- Entire grid: all rooms with their properties.
- Inventory: consumables (steps, gems, keys, dice, gold) and permanents
- Player: current position (row, col)
- Discovered vs undiscovered rooms

HOW TO LOAD:
============
1. Select ‘Charger Partie’ from the menu
2. Reads saves/save.json
3. Reconstructs the exact state of the game
"""

import json
import os
from typing import Any
from datetime import datetime

SAVE_DIR = "saves"
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")


def save_game(grid: Any, inventory: Any, player: Any, filename: str = SAVE_FILE) -> bool:

    try:
        # Crear carpeta saves/ si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Construir estructura de datos
        data = {}
        
        # ========================================
        # 1. SERIALIZAR GRID (todas las rooms)
        # ========================================
        cells = []
        for r in range(grid.rows):
            row = []
            for c in range(grid.cols):
                room = grid.get_room(r, c)
                is_discovered = grid.is_discovered(r, c)
                
                if room is None:
                    # Casilla vacía (no room aún)
                    row.append({
                        "exists": False,
                        "discovered": is_discovered
                    })
                else:
                    # Serializar room completa
                    row.append({
                        "exists": True,
                        "discovered": is_discovered,
                        "name": room.name,
                        "image_name": room.image_name,
                        "room_type": room.room_type,
                        "cost_gems": room.cost_gems,
                        "effect_data": room.effect_data,
                        "color_type": room.color_type,
                        "rarity": room.rarity,
                    })
            cells.append(row)
        
        data["grid"] = {
            "rows": grid.rows,
            "cols": grid.cols,
            "cells": cells
        }
        

        data["inventory"] = {

            "steps": inventory.steps,
            "gems": inventory.gems,
            "keys": inventory.keys,
            "dice": inventory.dice,
            "gold": inventory.gold,
            

            "permanents": {
                "shovel": inventory.shovel,
                "hammer": inventory.hammer,
                "picklock_kit": inventory.picklock_kit,
                "metal_detector": inventory.metal_detector,
                "rabbit_foot": inventory.rabbit_foot,
            }
        }
        

        data["player"] = {
            "row": player.row,
            "col": player.col
        }
        

        data["metadata"] = {
            "save_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "game_version": "1.0"
        }
        

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Partie sauvegardée: {filename}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False


def load_game(grid: Any, inventory: Any, player: Any, filename: str = SAVE_FILE) -> bool:
    """
    Carga una partida guardada desde JSON.
    
    Args:
        grid: Grid object (se modificará con datos cargados)
        inventory: Inventory object (se modificará)
        player: Player object (se modificará)
        filename: Ruta del archivo
    
    Returns:
        True si se cargó exitosamente, False si no existe o hay error
    """
    if not os.path.exists(filename):
        print(f" Aucune sauvegarde trouvée: {filename}")
        return False
    
    try:

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        

        grid_data = data.get("grid", {})
        cells = grid_data.get("cells", [])
        
        for r, row in enumerate(cells):
            for c, cell in enumerate(row):
                if cell.get("exists"):

                    from grid import Room
                    room = Room(
                        name=cell.get("name", "Unknown"),
                        image_name=cell.get("image_name"),
                        room_type=cell.get("room_type", "normal"),
                        cost_gems=cell.get("cost_gems", 0),
                        effect_data=cell.get("effect_data", {}),
                        color_type=cell.get("color_type", "neutral"),
                        rarity=cell.get("rarity", 0)
                    )
                    grid.grid[r][c] = room
                else:
                    grid.grid[r][c] = None
                

                grid.discovered[r][c] = cell.get("discovered", False)
        

        inv_data = data.get("inventory", {})
        inventory.steps = inv_data.get("steps", 70)
        inventory.gems = inv_data.get("gems", 2)
        inventory.keys = inv_data.get("keys", 0)
        inventory.dice = inv_data.get("dice", 0)
        inventory.gold = inv_data.get("gold", 0)
        
        perms = inv_data.get("permanents", {})
        inventory.shovel = perms.get("shovel", False)
        inventory.hammer = perms.get("hammer", False)
        inventory.picklock_kit = perms.get("picklock_kit", False)
        inventory.metal_detector = perms.get("metal_detector", False)
        inventory.rabbit_foot = perms.get("rabbit_foot", False)
        

        player_data = data.get("player", {})
        player.row = player_data.get("row", grid.rows - 1)
        player.col = player_data.get("col", 0)
        player.reset_cursor_to_player()
        

        metadata = data.get("metadata", {})
        save_date = metadata.get("save_date", "Unknown")
        print(f" Partie chargée (sauvegardée le: {save_date})")
        
        return True
        
    except Exception as e:
        print(f" Erreur lors du chargement: {e}")
        return False


def get_save_info(filename: str = SAVE_FILE) -> dict:
    """
    Obtiene información de una partida guardada sin cargarla.
    Útil para mostrar en el menú.
    
    Returns:
        dict con: save_date, steps, gold, position, etc.
    """
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        metadata = data.get("metadata", {})
        inv_data = data.get("inventory", {})
        player_data = data.get("player", {})
        
        return {
            "save_date": metadata.get("save_date", "Unknown"),
            "steps": inv_data.get("steps", 0),
            "gold": inv_data.get("gold", 0),
            "gems": inv_data.get("gems", 0),
            "position": f"({player_data.get('row', 0)}, {player_data.get('col', 0)})"
        }
    except:
        return None



if __name__ == "__main__":
    print("=" * 70)
    print("TEST")
    print("=" * 70)
    
    # Simular objetos del juego
    class MockGrid:
        def __init__(self):
            self.rows = 5
            self.cols = 9
            self.grid = [[None for _ in range(9)] for _ in range(5)]
            self.discovered = [[False for _ in range(9)] for _ in range(5)]
        
        def get_room(self, r, c):
            return self.grid[r][c]
        
        def is_discovered(self, r, c):
            return self.discovered[r][c]
    
    class MockInventory:
        def __init__(self):
            self.steps = 50
            self.gems = 3
            self.keys = 2
            self.dice = 1
            self.gold = 10
            self.shovel = True
            self.hammer = False
            self.picklock_kit = True
            self.metal_detector = False
            self.rabbit_foot = False
    
    class MockPlayer:
        def __init__(self):
            self.row = 3
            self.col = 4
        
        def reset_cursor_to_player(self):
            pass
    

    grid = MockGrid()
    inventory = MockInventory()
    player = MockPlayer()
    

    print("\nTest de guardado...")
    success = save_game(grid, inventory, player)
    
    if success:
        print("\nTest de carga...")

        inventory.steps = 0
        player.row = 0
        
        success2 = load_game(grid, inventory, player)
        
        if success2:
            print(f"\n Valores restaurados:")
            print(f"   Steps: {inventory.steps}")
            print(f"   Player pos: ({player.row}, {player.col})")
            print(f"   Shovel: {inventory.shovel}")
        
        # Test: Info
        print("\n Info de la partida guardada:")
        info = get_save_info()
        if info:
            for key, value in info.items():
                print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)