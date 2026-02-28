from random import choice, seed
seed(7030)
from typing import Optional

DAMAGE = "damage"
HEAT = "heat"
SHIELD = "shield"

CARD_NAME = "Card"
CARD_DESC = "A card."
SB_NAME = "Small Blast"
SB_DESC = "Deal 1 damage to target."
BB_NAME = "Big Blast"
BB_DESC = "Deal 5 damage to target, applying 3 heat."
RS_NAME = "Raise Shield"
RS_DESC = "Apply 5 Shield."
LE_NAME = "Leech Energy"
LE_DESC = "Heat target and raise shield by 2."

HARD_POINT_SYMBOL = "P"
LL_SYMBOL = "L"
HL_SYMBOL = "H"
SG_SYMBOL = "S"
RECHARGING_SYMBOL = "R"

DESTROYED_INTENT = "Hardpoint Inoperable!"
RECHARGING_INTENT = "Weapon Recharging!"

CONTROLLER_DESC = "A game of Breachway using: "
WELCOME_MESSAGE = "Welcome to BreachWay!"
ENCOUNTER_MESSAGE = "New encounter!"
NO_ENERGY_MESSAGE = "Insufficent energy"
TURN_END_MESSAGE = "Turn ended."
ENEMY_ACTION_MESSAGE = "The enemy has responded!"
ENCOUNTER_WIN_MESSAGE = "Enemy destroyed!"
WIN_MESSAGE = "The sector is yours, you are victorious!"
LOSS_MESSAGE = "You have been destroyed..."

HELP_COMMAND = "help"
CHECK_COMMAND = "check deck"
END_TURN_COMMAND = "end turn"
PLAY_CARD_COMMAND = "play card"
LOAD_COMMAND = "load"

COMMAND_PROMPT = "Please enter command (or Help to see valid commands): "
HARDPOINT_PROMPT = "Please enter target hardpoint number: "

INVALID_COMMAND = ("Invalid command! Enter 'Help' to see a list of valid"
                   " commands.")
INVALID_HARDPOINT = "Invalid target."
INVALID_INT = "Please enter an integer."

CORRPUT_FILE = "Invalid or Corrupted Game file: "
NO_FILE = "Could not find file: "
PLAYER_COUNT_CORRUPT = "Incorrect number of players"
CORRUPT_ARMOUR = "Invalid armour value"
CORRUPT_ENERGY = "Invalid player energy value"
CORRUPT_HARDPOINT_COUNT = "Ship cannot have 0 hardpoints"
CORRPUT_HARDPOINT = "Invalid hardpoint"
CORRUPT_ENEMY_COUNT = "Cannot have 0 enemies"

HELP_MESSAGES = ["Commands:",
                 "  - Help: See possible commands.", 
                 "  - Check deck: List cards in deck, with their cooldowns.",
                 "  - Play card X: Plays Card at position X in hand.",
                 "  - End turn: end your turn and let the enemy move."
                 ] 

MAX_HAND = 5

SAVE_LOC = "autosave.txt"

def shuffle_cards(card_list: list["Card"]):
    """
    Shuffles a list of cards in place (that is, mutates the given list).

    Shuffles in a consistent manner that should hopefully minimise issues
    with Gradescope desynchs. You are not expected to understand this method.

    Args:
        card_list (list[Card]): list of cards that will be shuffled in place.
    """

    card_types = []
    to_choose = {}

    # Sort cards into groups so random sampling is consistent
    while card_list:
        curr_card = card_list.pop()
        curr_name = curr_card.get_name()
        if curr_name not in to_choose:
            card_types.append(curr_name)
            to_choose[curr_name] = [curr_card]
        else:
            # Check for ailiasing to prevent nasty bugs later on
            if any(card is curr_card for card in to_choose[curr_name]):
                raise ValueError(
                    "You have multiple references to the same card." + 
                    " Please ensure each card is being created "
                    "as a new instance."
                )
            
            else:
                to_choose[curr_name].append(curr_card)
    
    card_types.sort() # ensure consistency regardless of initial card order
    
    # Replace cards in a random order
    while to_choose:
        key = choice(card_types)
        new_card = to_choose[key].pop()

        if not to_choose[key]:
            to_choose.pop(key)
            card_types.remove(key)
        
        card_list.append(new_card)
