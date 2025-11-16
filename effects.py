"""
effects.py - Apply room effects when player enters.
OBJECTS (food, tools) are INSIDE rooms, not rooms themselves.
"""

def apply_room_effect(room, player, inventory, grid):
    """
    Apply room effect when player enters.
    Rooms can contain objects that activate upon entry.
    """
    if room is None:
        return "Salle vide."

    t = room.room_type
    effect_data = room.effect_data

    # ---- LOCKED ROOM (requires key to enter - already consumed in modal) ----
    
    if t == "locked_room":
        # Key already consumed in _handle_modal_key
        gold = effect_data.get("gold", 10)
        gems = effect_data.get("gems", 2)
        inventory.gold += gold
        inventory.gems += gems
        return f"Coffre-fort ouvert! Vous trouvez {gold} pièces d'or et {gems} gemmes!"

    # ---- ROOMS THAT GIVE RESOURCES DIRECTLY ----
    
    if t == "bibliotheque":
        # Library - gives gems
        gems = effect_data.get("gems", 1)
        inventory.gems += gems
        return f"Vous trouvez {gems} gemme(s) dans la bibliothèque."
    
    if t == "atelier":
        # Workshop - gives keys
        keys = effect_data.get("keys", 1)
        inventory.keys += keys
        return f"Vous trouvez {keys} clé(s) dans l'atelier."
    
    if t == "tresor":
        # Treasure room - gives gold
        gold = effect_data.get("gold", 5)
        inventory.gold += gold
        return f"Vous trouvez {gold} pièces d'or dans le trésor!"

    # ---- ROOMS WITH FOOD (object inside room) ----
    
    if t == "bedroom" and effect_data.get("has_food"):
        # Bedroom with food - randomly draw which food
        import random
        food_options = [
            ("une pomme", 2),
            ("une banane", 3),
            ("un gâteau", 10),
        ]
        food_name, steps = random.choice(food_options)
        inventory.steps += steps
        return f"Vous trouvez {food_name} et récupérez {steps} pas."

    # ---- ROOMS WITH TRAPS ----
    
    if t == "piege":
        damage = effect_data.get("trap_damage", 5)
        inventory.steps -= damage
        return f"Un piège! Vous perdez {damage} pas."

    # ---- ROOMS WITH CONTAINERS (interactive objects) ----
    
    if t == "coffre":
        # Room with chests - requires key or hammer
        chest_count = effect_data.get("chest_count", 1)
        if inventory.keys > 0:
            inventory.keys -= 1
            # Chest reward
            import random
            reward_type = random.choice(["gold", "food", "gems"])
            if reward_type == "gold":
                inventory.gold += 5
                return f"Vous ouvrez un coffre avec une clé et trouvez 5 pièces d'or."
            elif reward_type == "food":
                inventory.steps += 10
                return f"Vous ouvrez un coffre avec une clé et trouvez de la nourriture (+10 pas)."
            else:
                inventory.gems += 1
                return f"Vous ouvrez un coffre avec une clé et trouvez 1 gemme."
        elif inventory.hammer:
            # With hammer, no key needed
            import random
            reward_type = random.choice(["gold", "food", "gems"])
            if reward_type == "gold":
                inventory.gold += 5
                return f"Vous brisez le coffre avec le marteau et trouvez 5 pièces d'or."
            elif reward_type == "food":
                inventory.steps += 10
                return f"Vous brisez le coffre avec le marteau et trouvez de la nourriture (+10 pas)."
            else:
                inventory.gems += 1
                return f"Vous brisez le coffre avec le marteau et trouvez 1 gemme."
        else:
            return f"Il y a {chest_count} coffre(s), mais vous n'avez ni clé ni marteau."
    
    if t == "casier":
        # Locker room - requires key
        locker_count = effect_data.get("locker_count", 2)
        if inventory.keys > 0:
            inventory.keys -= 1
            inventory.steps += 8
            return f"Vous ouvrez un casier avec une clé et trouvez de la nourriture (+8 pas)."
        else:
            return f"Il y a {locker_count} casiers fermés. Vous avez besoin d'une clé."
    
    if t == "creuser":
        # Dig spot - requires shovel
        dig_spots = effect_data.get("dig_spots", 1)
        if inventory.shovel:
            import random
            reward_type = random.choice(["gold", "gems", "nothing"])
            if reward_type == "gold":
                inventory.gold += 3
                return f"Vous creusez avec la pelle et trouvez 3 pièces d'or."
            elif reward_type == "gems":
                inventory.gems += 1
                return f"Vous creusez avec la pelle et trouvez 1 gemme."
            else:
                return f"Vous creusez avec la pelle, mais ne trouvez rien."
        else:
            return f"Il y a {dig_spots} endroit(s) où creuser, mais vous n'avez pas de pelle."

    # ---- ROOMS WITH PERMANENT ITEMS ----
    
    if effect_data.get("item"):
        # Room containing a permanent item
        item = effect_data.get("item")
        if item == "pelle" and not inventory.shovel:
            inventory.shovel = True
            return "Vous trouvez une pelle!"
        elif item == "marteau" and not inventory.hammer:
            inventory.hammer = True
            return "Vous trouvez un marteau!"
        elif item == "crochetage" and not inventory.picklock_kit:
            inventory.picklock_kit = True
            return "Vous trouvez un kit de crochetage!"
        elif item == "detecteur" and not inventory.metal_detector:
            inventory.metal_detector = True
            return "Vous trouvez un détecteur de métaux!"
        elif item == "patte_lapin" and not inventory.rabbit_foot:
            inventory.rabbit_foot = True
            return "Vous trouvez une patte de lapin!"
        else:
            return f"Cette salle contenait un objet, mais vous l'avez déjà."

    # ---- EXIT (WIN) ----
    
    if t == "exit":
        return "Vous avez atteint l'Antichambre! Victoire!"

    # ---- NEUTRAL OR NO EFFECT ROOMS ----
    
    return f"Vous entrez dans {room.name}. Rien de spécial ici."