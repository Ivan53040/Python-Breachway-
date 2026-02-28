# DO NOT modify or add any import statements
from support import *
from display import BreachView

# Name:Kung Tsz Fung
# Student Number: 48996066
# Favorite Building: Tokyo Skytree
# -----------------------------------------------------------------------------


# Write your classes and functions here

#region Model---------------------------------------------------------------------------

class Card():
    """
    Base class for all cards, each card has a name, 
    description, cost, cooldown, and effect.
    """
    def __init__(self):
        self._name = CARD_NAME
        self._description = CARD_DESC
        self._cost = 1
        self._cooldown = 1
        self._effect = {}

    def get_name(self) -> str:
        """
        Returns the name of the card.
        """
        return self._name

    def get_cost(self) -> int:
        """
        Returns the cost of the card.
        """
        return self._cost

    def get_cooldown(self) -> int:
        """
        Returns the cooldown of the card.
        """
        return self._cooldown

    def get_effect(self) -> dict[str, int]:
        """
        Returns the effect of the card.
        """
        return self._effect

    def __str__(self) -> str:
        """
        Returns the string representation of the card.
        Which is the name of the card with its description.
        """
        return f"{self._name}: {self._description}"

    def __repr__(self) -> str:
        """
        Returns the representation of the card.
        Which is the name of the card.
        """
        return f"{self.__class__.__name__}()"

class SmallBlast(Card):
    """
    SmallBlast is a Card that deals 1 damage to the enemy,
    has a cost of 1, cooldown of 1 and its own symbol.
    """
    def __init__(self):
        super().__init__()
        self._name = SB_NAME
        self._description = SB_DESC
        self._cost = 1
        self._cooldown = 1
        self._effect = {"damage": 1}

class BigBlast(Card):
    """
    BigBlast is a Card that deals 5 damage to the enemy,
    has a cost of 3, cooldown of 4 and its own symbol.
    """
    def __init__(self):
        super().__init__()
        self._name = BB_NAME
        self._description = BB_DESC
        self._cost = 3
        self._cooldown = 4
        self._effect = {"damage": 5, "heat": 3}

class RaiseShield(Card):
    """
    RaiseShield is a Card that raises the shield of the player by 5,
    has a cost of 1, cooldown of 2 and its own symbol.
    """
    def __init__(self):
        super().__init__()
        self._name = RS_NAME
        self._description = RS_DESC
        self._cost = 1
        self._cooldown = 2
        self._effect = {"shield": 5}

class LeechEnergy(Card):
    """
    LeechEnergy is a Card that deals 2 damage to the enemy,
    has a cost of 2, cooldown of 3 and its own symbol.
    """
    def __init__(self):
        super().__init__()
        self._name = LE_NAME
        self._description = LE_DESC
        self._cost = 2
        self._cooldown = 3
        self._effect = {"shield": 2, "heat": 2}

class CardDeck():
    """
    CardDeck is a class that represents a deck of cards.
    It manages the player's card and cooldown states.
    """
    def __init__(self, cards: list[tuple[Card, int]]):
        """
        Initialises the CardDeck with a list of cards and cooldowns.
        """
        self._cards = []
        for card, cooldown in cards:
            self._cards.append((card, cooldown))
            
    def draw_cards(self, num_cards: int) -> list[Card]:
        """
        Draws a specific number of cards from the deck when the cooldown is 0.
        Returns a list of cards drawn.
        """
        drawn = []
        new_cards = []
        for card, cooldown in self._cards:
            if cooldown == 0 and len(drawn) < num_cards:#draw the card if the cooldown is 0
                drawn.append(card)
            else:
                new_cards.append((card, cooldown))#add the card to the new cards list
        self._cards = new_cards
        return drawn
    
    
    def add_card(self, card: Card) -> None:
        """
        Adds a card to the deck and sets its cooldown to the card's cooldown.
        """
        self._cards.append((card, card.get_cooldown()))
        
    def advance_cards(self) -> None:
        """
        Reduces the cooldown of each card by 1,
        if the cooldown is 0, it is set to 0.
        """
        updated_cards = []
        for card, cooldown in self._cards:
            if cooldown >= 1:#reduce the cooldown by 1 if it is greater than 0
                new_cooldown = cooldown - 1
            else:
                new_cooldown = 0#set the cooldown to 0 if it is 0
            updated_cards.append((card, new_cooldown))
        self._cards = updated_cards

    def __str__(self) -> str:
        """
        Returns a string representation of the deck,
        showing the cards that are ready to be played 
        and the cards that are on cooldown.
        """
        ready = []
        not_ready = {}

        for card, cooldown in self._cards:
            if cooldown == 0:#put the card in the ready list if the cooldown is 0
                ready.append(card.get_name())
                
            else:#put the card in the not ready list if the cooldown is not 0
                not_ready.setdefault(cooldown, []).append(card.get_name())
        return_list = []

        if ready:#put the ready list in the return list
            return_list.append("Ready: " + ", ".join(ready))

        for cooldown in sorted(not_ready):#put the not ready list in the return list
            return_list.append(f"Cooldown {cooldown}: " + \
                               ", ".join(not_ready[cooldown]))


        return "; ".join(return_list)#return the return list

    def __repr__(self) -> str:
        """
        Returns the representation of the deck.
        The card and cooldown are sorted by cooldown and index.
        """
        sorted_cards = sorted(
            [(i, card, cd) for i, (card, cd) in enumerate(self._cards)],
            key=lambda x: (x[2], x[0])
        )#sort the cards by cooldown and index
        return "CardDeck([" + ", ".join(f"({repr(card)}, {cd})" \
                                        for _, card, cd in sorted_cards) + "])"

class HardPoint():
    """
    HardPoint is a class that represents a hardpoint on the ship.
    It has a name, a list of cards, a maximum armour, a current armour,
    a symbol.
    The order used to determine which card to use.
    """
    def __init__(self):
        self._name = "Hardpoint"
        self._card = [SmallBlast()] 
        self._max_armour = 1
        self._armour = self._max_armour
        self._symbol = HARD_POINT_SYMBOL
        self._order = 0
    
    def get_cards(self) -> list[Card]:
        """
        Returns the list of cards on the hardpoint.
        """
        return self._card
    
    def get_armour(self) -> int:
        """
        Returns the current armour of the hardpoint.
        """
        return self._armour

    def is_functional(self) -> bool:
        """
        Returns True if the hardpoint is functional, False otherwise.
        """
        return self._armour > 0
    
    def damage(self, damage: int) -> None:
        """
        Reduces the armour of the hardpoint by the damage amount,
        but not below 0.
        """
        self._armour = max(0,min(self._armour - damage, self._max_armour))

    def repair(self) -> None:
        """
        Repairs the hardpoint to its maximum armour.
        """
        self._armour = self._max_armour
    
    def enemy_action(self) -> dict[str, int]:
        """
        Returns the effect of the card on the enemy.
        """
        if not self.is_functional():#if the enemy is destroyed, return an empty dictionary
            return {}
        card = self._card[self._order]
        self._order += 1
        if self._order == len(self._card):
            self._order = 0#if the order is the length of the card, set the back to 0
        return card.get_effect()#return the effect of the card
        
        
    def enemy_intent(self) -> str:
        """
        Returns the intent of the hardpoint.
        """
        if not self.is_functional():#if the enemy is destroyed, return the destroyed intent
            return DESTROYED_INTENT
        return str(self._card[self._order])#return the intent of the card

    
    def __str__(self) -> str:
        """
        Returns the string representation of the hardpoint.
        Which is the symbol of the hardpoint.
        """
        return f"{self._symbol}"
    
    def __repr__(self) -> str:
        """
        Returns the representation of the hardpoint.
        Which is the name of the hardpoint.
        """
        return f"{self.__class__.__name__}()"

class LightLaser(HardPoint):
    """
    LightLaser is a HardPoint that has 3 SmallBlast cards and 1 BigBlast card.
    """
    def __init__(self):
        super().__init__()
        self._name = "Light Laser"
        self._symbol = LL_SYMBOL
        self._card = [SmallBlast(), SmallBlast(), SmallBlast(), BigBlast()]

class ShieldGenerator(HardPoint):
    """
    ShieldGenerator is a HardPoint that has 2 RaiseShield cards 
    and 1 LeechEnergy card. With a maximum armour of 2.
    """
    def __init__(self):
        super().__init__()
        self._max_armour = 2
        self._armour = self._max_armour
        self._name = "Shield Generator"
        self._symbol = SG_SYMBOL
        self._card = [RaiseShield(), RaiseShield(), LeechEnergy()]

class HeavyLaser(HardPoint):
    """
    HeavyLaser is a HardPoint that has 2 BigBlast cards.
    It has a maximum armour of 3.
    It has a can_fire attribute that is True if the hardpoint can fire,
    False otherwise. The can_fire attribute changes every turn.
    """
    def __init__(self, can_fire: bool):
        """
        Initialises the HeavyLaser with a can_fire attribute 
        with a default value of True. It has the symbol of the hardpoint
        if can_fire is True, otherwise it has the recharging symbol.
        """
        super().__init__()
        self._max_armour = 3
        self._armour = self._max_armour
        self._name = "Heavy Laser"
        self._can_fire = can_fire
        self._symbol = HL_SYMBOL if can_fire else RECHARGING_SYMBOL
        self._card = [BigBlast(),BigBlast()]

    def enemy_action(self) -> dict[str, int]:
        """
        Returns the effect of the card on the enemy.
        The effect is affected by the can_fire attribute.
        """
        if not self.is_functional():#if the enemy is destroyed, return an empty dictionary
            return {}
        if self._can_fire == False:#if the can_fire attribute is False, set it to True.
            self._can_fire = True
            self._symbol = HL_SYMBOL
            return {}
        
        card = self._card[self._order]
        self._order += 1#fire action, set the can_fire to False after firing
        self._can_fire = False
        self._symbol = RECHARGING_SYMBOL

        if self._order == len(self._card):#if the order reach the length of the card
            self._order = 0#set that back to 0
        return card.get_effect()
        
    def enemy_intent(self) -> str:
        """
        Returns the intent of the hardpoint.
        The intent is affected by the can_fire attribute.
        """
        if not self.is_functional():#if the enemy is destroyed, return the destroyed intent
            return DESTROYED_INTENT
        if self._can_fire == False:#if the can_fire attribute is False, 
            return RECHARGING_INTENT#return the recharging intent
        return str(self._card[self._order])
    
    def __repr__(self) -> str:
        """
        Returns the representation of the hardpoint.
        Which is the name of the hardpoint and the can_fire attribute.
        """
        return f"{self.__class__.__name__}({self._can_fire})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the hardpoint.
        Which is the symbol of the hardpoint.
        """
        return self._symbol


class Ship():
    """
    Ship is a class that represents a ship.
    It has a list of hardpoints, a current armour,
    a shield and a heat.
    """
    def __init__(self, armour: int, hardpoints: list[HardPoint]):
        """
        Initialises the ship with a list of hardpoints,
        a current armour, a shield and a heat.
        """
        self._hardpoints = hardpoints
        self._armour = armour
        self._shield = 0
        self._heat = 0

    def get_hardpoints(self) -> list[HardPoint]:
        """
        Returns the list of hardpoints on the ship.
        """
        return self._hardpoints

    def get_armour(self) -> int:
        """
        Returns the current armour of the ship.
        """
        return self._armour
    
    def get_shield(self) -> int:
        """
        Returns the current shield of the ship.
        """
        return self._shield
    
    def get_heat(self) -> int:
        """
        Returns the current heat of the ship.
        """
        return self._heat
    
    def is_destroyed(self) -> bool:
        """
        Returns True if the ship is destroyed, False otherwise.
        """
        return self._armour == 0
    
    def apply_shield(self, shield_points: int) -> None:
        """
        Applies the shield points to the ship's shield.
        """
        self._shield += shield_points
        
    def apply_heat(self, heat: int) -> None:
        """
        Applies the heat to the ship's heat.
        """
        while heat > 0 and self._shield > 0:#1.apply heat to the shield first
            self._shield -= 1
            heat -= 1
        self._heat += heat#2.apply the remaining heat to the heat

    def apply_damage(self, damage: int, hard_point: HardPoint) -> None:
        """
        Applies the damage to the ship.
        """
        while damage > 0 and self._shield > 0:# 1. Apply shield first
            self._shield -= 1
            damage -= 1

        if damage > 0 and hard_point.is_functional():
            # 2. Apply to hardpoint (half, rounded up)
            hp_damage = (damage + 1) // 2
            hard_point.damage(hp_damage)
            damage -= hp_damage

        # 3. Apply the remaining damage to the ship
        self._armour = max(0, self._armour - damage)


    def reset_status(self) -> None:
        """
        Resets the ship's shield, heat and hardpoints.
        """
        self._shield = 0
        self._heat = 0
        for hardpoint in self._hardpoints:#repair the hardpoints to the maximum armour
            hardpoint.repair()
    
    def new_turn(self) -> None:
        """
        New turn for the ship.
        Repairs the functional hardpoints and applies the heat to the ship.
        Shields are halved.
        """
        for hardpoint in self._hardpoints:#repair the hardpoints to the maximum armour
            if not hardpoint.is_functional():
                hardpoint.repair()

        if self._heat > 0:#apply the heat to the ship
            self._armour = max(0, self._armour - self._heat)
            self._heat -= 1


        self._shield = self._shield//2#halve the shield


    def __str__(self) -> str:
        """
        Returns the string representation of the ship.
        Which is the armour, the hardpoints and the heat.
        """
        return f"{self._armour},"+",".join(str(hp) for hp in self._hardpoints)
    
    def __repr__(self) -> str:
        """
        Returns the representation of the ship.
        Which is the name of the ship, the armour and the hardpoints.
        """
        return f"{self.__class__.__name__}({self._armour}, {self._hardpoints})"

class Player(Ship):
    """
    Player is a Ship that has a list of hardpoints and a current energy.
    """
    def __init__(self, armour: int, hardpoints: list[HardPoint], intial_energy: int):
        """
        Initialises the player with a list of hardpoints,
        a current armour, a shield and a heat.
        With a special energy attribute that use to pay for the cards.
        """
        super().__init__(armour, hardpoints)
        self._energy = intial_energy
    
    def new_turn(self) -> None:
        """
        New turn for the player.
        The energy is increased by 1 for each functional hardpoint.
        """
        for hardpoint in self._hardpoints:
            if hardpoint.is_functional() == True:
                self._energy += 1
        super().new_turn()

    def build_deck(self) -> CardDeck:
        """
        Builds a deck of cards for the player.
        """
        all_cards = []
        for hp in self._hardpoints:#get the cards from the hardpoints
            for card in hp.get_cards():
                all_cards.append(type(card)())

        shuffle_cards(all_cards)#shuffle the cards

        return CardDeck([(card, 0) for card in all_cards])
        
    def get_energy(self) -> int:
        """
        Returns the current energy of the player.
        """
        return self._energy
    
    def spend_energy(self, energy: int) -> bool:
        """
        Spends the energy of the player.
        Returns True if the energy is enough and spent, False otherwise.
        """
        if energy <= self._energy:#if the energy is enough, spend the energy
            self._energy -= energy
            return True#return True so the card can be played
        else:
            return False#if the energy is not enough, return False
    
    def __str__(self) -> str:
        """
        Returns the string representation of the player.
        Which is the armour, the hardpoints and the energy.
        """
        return f"{self._armour},"+",".join(str(hp) for hp in self._hardpoints)+\
            ","+str(self._energy)
    
    def __repr__(self) -> str:
        """
        Returns the representation of the player.
        Which is the name of the player, the armour and the hardpoints.
        """
        return f"Player({self._armour}, {self._hardpoints}, {self._energy})"

class Enemy(Ship):
    """
    Enemy is a ship that player play against, it has a list of hardpoints.
    """
    def __init__(self, armour: int, hardpoints: list[HardPoint]):
        super().__init__(armour, hardpoints)

    def get_intents(self) -> list[tuple[HardPoint,str]]:
        """
        Return the enemy's intent for each hardpoint.
        """
        return [(hp, hp.enemy_intent()) for hp in self._hardpoints]
    
    def get_actions(self) -> list[dict[str,int]]:
        """
        Return the enemy's action for each hardpoint.
        """
        return [hp.enemy_action() for hp in self._hardpoints]
    
class BreachModel():
    """
    BreachModel is a class that represents the game model.
    It has a player, a list of enemies, a deck, a hand,
    an active enemy and a remaining enemy count.
    """
    def __init__(self, player: Player, enemies: list[Enemy]):
        self._player = player
        self._enemies = enemies
        self._deck = None
        self._hand = []
        self._active_enemy = None

    def get_player(self) -> Player:
        """
        Returns the model of the player.
        """
        return self._player
    
    def get_enemies(self) -> list[Enemy]:
        """
        Returns the list of enemies in the model.
        """
        return self._enemies
    
    def get_deck(self) -> Optional[CardDeck]:
        """
        Returns the deck of the model.
        """
        return self._deck
    
    def get_hand(self) -> list[Card]:
        """
        Returns the hand of the model.
        """
        return self._hand
    
    def get_active_enemy(self) -> Optional[Enemy]:
        """
        Returns the active enemy of the model.
        """
        return self._active_enemy
    
    def get_remaining_enemy_count(self) -> int:
        """
        Returns the remaining enemy count of the model.
        """
        return sum(not enemy.is_destroyed() for enemy in self._enemies)

    def has_won(self) -> bool:
        """
        Returns True if the player has won, False otherwise.
        """
        return self.get_remaining_enemy_count() == 0 and not self._player.is_destroyed()

    def has_lost(self) -> bool:
        """
        Returns True if the player has lost, False otherwise.
        """
        return self._player.is_destroyed()
    
    def new_encounter(self) -> None:
        """
        Starts a new encounter.
        Resets the player's status, 
        builds a deck, draws cards 
        and sets the active enemy.
        """
        for enemy in self._enemies:
            if not enemy.is_destroyed():
                self._active_enemy = enemy
                self._player.reset_status()
                self._deck = self._player.build_deck()
                self._hand = self._deck.draw_cards(MAX_HAND)
                break
                
    def encounter_ongoing(self) -> bool:
        """
        Returns True there is a active enemy,
        the player is not destroyed 
        and the enemy is not destroyed.
        """
        return self._active_enemy is not None and \
            not self._player.is_destroyed() and \
                not self._active_enemy.is_destroyed()
    
    def play_card(self, card: Card, target_hardpoint: HardPoint) -> bool:
        """
        Play card action, 
        1. check if the card is in hand,
        2. check if the player has enough energy,
        3. remove the card from the hand,
        4. add the card back to the deck,
        5. apply the effects of the card to the player and the enemy.
        6. Returns True if the card is played.
        """
        if card not in self._hand:#step 1
            return False
        if not self._player.spend_energy(card.get_cost()):#step 2
            return False
        self._hand.remove(card)#step 3
        self._deck.add_card(card)#step 4

        effects = card.get_effect()#step 5
        if SHIELD in effects:
            self._player.apply_shield(effects[SHIELD])
        if HEAT in effects:
            self._active_enemy.apply_heat(effects[HEAT])
        if DAMAGE in effects:
            self._active_enemy.apply_damage(effects[DAMAGE], target_hardpoint)
        return True#step 6
    
    def end_turn(self) -> None:
        """
        End turn action,
        1. get the actions of the active enemy,
        2. apply the effects of the actions to the player from the enemy.
        3. player and enemy(if not destroyed) get new turn.
        4. deck advances cards,
        5. draw cards(up to MAX_HAND) to the hand.
        """
        actions = self._active_enemy.get_actions()#Step 1
        for effect in actions:#Step 2
            if DAMAGE in effect:
                enemy_targets = [hp for hp in self._player.get_hardpoints() \
                                 if hp.is_functional()]
                if enemy_targets:
                    target = min(enemy_targets, \
                                 key=lambda hp: (hp.get_armour(), \
                                                 self._player.get_hardpoints().index(hp)))
                    self._player.apply_damage(effect[DAMAGE], target)
            if HEAT in effect:
                self._player.apply_heat(effect[HEAT])
            if SHIELD in effect:
                self._active_enemy.apply_shield(effect[SHIELD])
        
        self._player.new_turn()#Step 3
        if self._active_enemy is not None:
            self._active_enemy.new_turn()

        self._deck.advance_cards()#Step 4
        cards = MAX_HAND - len(self._hand)
        self._hand.extend(self._deck.draw_cards(cards))#Step 5


    def __str__(self) -> str:
        """
        Returns the string representation of the model.
        Which is the player and the enemies.
        """
        enemy_str = ";".join(str(enemy) for enemy in self._enemies)
        return f"{str(self._player)}|{enemy_str}"
    
    def __repr__(self) -> str:
        """
        Returns the representation of the model.
        Which is the player and the enemies.
        """
        return f"BreachModel({repr(self._player)}, {repr(self._enemies)})"
#endregion  

#region Controller------------------------------------------------------------------------
class BreachWay():
    """
    BreachWay is a class that represents the game controller.
    It has a file, a model, a view and a controller.
    """
    def __init__(self, file:str):
        self._file = file
        self._model = self.load_game(file)
        self._view = BreachView()

    def update_display(self, messages: list[str]) -> None:
        """
        Update the display of the game.
        Get the player, the hand, the enemy and the messages.
        """
        player = self._model.get_player()
        hand = self._model.get_hand()
        enemy = self._model.get_active_enemy()
        self._view.display_game(player, enemy, hand, messages)

    def get_command(self) -> str:
        """
        1. Get the command from the user.
        2. Check if the command is valid,
        3. if not, update the display with the invalid command message.
        """
        while True:#step 1
            command = input(COMMAND_PROMPT).strip().lower()#step 2
            if command in [HELP_COMMAND, CHECK_COMMAND, END_TURN_COMMAND] or\
                command.startswith(PLAY_CARD_COMMAND) or command.startswith(LOAD_COMMAND):
                return command#check if the command is in the valid command list
            self.update_display([INVALID_COMMAND])#step 3
    
    def get_target_hardpoint(self) -> int:
        """
        1. Get the target hardpoint from the user.
        2. Check if the target hardpoint is valid,
        3. if not, update the display with the invalid hardpoint message.
        """
        while True:#step 1
            try:
                index = int(input(HARDPOINT_PROMPT)) -1#step 2
            except ValueError:
                self.update_display([INVALID_INT])
                continue
            enemy = self._model.get_active_enemy()
            if 0 <= index < len(enemy.get_hardpoints()):
                return index
            self.update_display([INVALID_HARDPOINT])#step 3 

    def save_game(self) -> None:
        """
        Save the game.
        """
        with open(SAVE_LOC, "w") as file:
            file.write(str(self._model))

    def load_game(self, file:str) -> BreachModel:
        """
        Load the game.
        Check if the file is found,
        if not, raise a FileNotFoundError.
        Check if the player count is correct,
        if not, raise a ValueError.
        Split the line into player and enemy.
        Make the ship objects.
        Return the model.
        """
        try:
            with open(file, "r") as file:
                line = file.readline().strip()
        except FileNotFoundError:
            raise FileNotFoundError(NO_FILE + file)
        
        if line.count("|") !=1:
            raise ValueError(PLAYER_COUNT_CORRUPT)
        
        player_str, enemy_str = line.split("|")
        def make_ship(s: str, is_player=False):
            """
            Make the ship objects.
            1. Split the line into parts.
            2. Check if the armour is valid,
            3. if not, raise a ValueError.
            4. Check if the energy is valid,
            5. if not, raise a ValueError.
            6. Make the ship's hardpoints.
            """
            parts = s.split(',')#step 1
            try:#step 2,3
                armour = int(parts[0])
                if armour < 0:
                    raise ValueError(CORRUPT_ARMOUR)
            except:
                raise ValueError(CORRUPT_ARMOUR)

            if is_player:#step 4,5
                try:
                    energy = int(parts[-1])
                    if energy < 0:
                        raise ValueError(CORRUPT_ENERGY)
                except:
                    raise ValueError(CORRUPT_ENERGY)
                hardpoints = parts[1:-1]
            else:
                hardpoints = parts[1:]

            if not hardpoints:
                raise ValueError(CORRUPT_HARDPOINT_COUNT)

            hp_objs = []
            for h in hardpoints:#step 6
                if h == LL_SYMBOL:
                    hp_objs.append(LightLaser())
                elif h == HL_SYMBOL:
                    hp_objs.append(HeavyLaser(True))
                elif h == RECHARGING_SYMBOL:
                    hp_objs.append(HeavyLaser(False))
                elif h == SG_SYMBOL:
                    hp_objs.append(ShieldGenerator())
                elif h == HARD_POINT_SYMBOL:
                    hp_objs.append(HardPoint())
                else:
                    raise ValueError(CORRPUT_HARDPOINT)
            #return the ship object with energy if it is the player, 
            #otherwise return the ship object without energy
            return Player(armour, hp_objs, energy) if is_player else Enemy(armour, hp_objs)
        
        #make the player ship object
        player = make_ship(player_str, is_player=True)
        #make the enemy ship objects
        enemies = [make_ship(e_str) for e_str in enemy_str.split(';') if e_str.strip()]

        if not enemies:#check if the enemy count is correct
            raise ValueError(CORRUPT_ENEMY_COUNT)

        return BreachModel(player, enemies)#return the model
    
    def play(self):
        """
        Play game action,
        1. start a new encounter,
        2. display the initial messages,
        3. get the command from the user,
        4. update the display with the command.
        5. check the win and loss condition,
        6. if the player has won, display the win message,
        7. if the player has lost, display the loss message,
        8. if the player has not won or lost, back to step 3.
        """
        self._model.new_encounter()#step 1
        remaining = self._model.get_remaining_enemy_count()
        self.update_display([WELCOME_MESSAGE,\
             ENCOUNTER_MESSAGE,f"{remaining} enemies remain..."])#step 2

        while not self._model.has_won() and not self._model.has_lost():#step 3
            command = self.get_command()
            messages = []

            if command == HELP_COMMAND:#help action
                self.update_display(HELP_MESSAGES)

            elif command == CHECK_COMMAND:#check action
                deck_str = str(self._model.get_deck())
                self.update_display(deck_str.split("; "))

            elif command == END_TURN_COMMAND:#end turn action
                self._model.end_turn()
                if self._model.has_lost():#check if the player has lost
                    messages = [TURN_END_MESSAGE, ENEMY_ACTION_MESSAGE, LOSS_MESSAGE]
                    self.update_display(messages)
                    return
                messages = [TURN_END_MESSAGE, ENEMY_ACTION_MESSAGE]
                #check if the enemy is destroyed and the encounter is ongoing
                enemy_destroyed = not self._model.encounter_ongoing() and \
                    self._model.get_active_enemy() is not None and \
                        self._model.get_active_enemy().is_destroyed()
                #if the enemy is destroyed, add the encounter win message
                if enemy_destroyed:
                    messages.append(ENCOUNTER_WIN_MESSAGE)
               
                if not self._model.encounter_ongoing():#check if the encounter is ongoing
                    self.save_game()
                    self._model.new_encounter()
                    if self._model.has_won():#check if the player has won
                        messages.append(WIN_MESSAGE)
                        self.update_display(messages)
                        return
                    messages.append(ENCOUNTER_MESSAGE)
                    remaining = self._model.get_remaining_enemy_count() 
                    messages.append(f"{remaining} enemies remain...")
                self.update_display(messages)

            elif command.startswith(PLAY_CARD_COMMAND):#play card action
                parts = command.split()
                if len(parts) != 3 or not parts[2].isdigit():#check if the command is valid
                    messages = [INVALID_COMMAND]
                    self.update_display(messages)
                else:
                    idx = int(parts[2]) - 1#get the index of the card
                    hand = self._model.get_hand()
                    if 0 <= idx < len(hand):#check if the index is valid
                        card = hand[idx]
                        target = 0
                        if DAMAGE in card.get_effect():
                            target = self.get_target_hardpoint()
                        if self._model.play_card(card, self._model.get_active_enemy()\
                                                 .get_hardpoints()[target]):
                            messages.append(f"Played {card.get_name()}.")
                        else:
                            messages.append(NO_ENERGY_MESSAGE)
                        self.update_display(messages)
                    else:
                        messages = [INVALID_COMMAND]
                        self.update_display(messages)
                    
                

            elif command.startswith(LOAD_COMMAND):#load game action
                parts = command.split(maxsplit=1)
                if len(parts) == 2:#check if the command is valid
                    try:
                        self._model = self.load_game(parts[1])
                        self._model.new_encounter()
                        messages = [ENCOUNTER_MESSAGE]
                    except FileNotFoundError:
                        messages = [NO_FILE + parts[1]]
                    except ValueError as ve:
                        messages = [str(ve)]
                    self.update_display(messages)

            

        if self._model.has_lost():#check if the player has lost
            messages = [TURN_END_MESSAGE, ENEMY_ACTION_MESSAGE, LOSS_MESSAGE]
        elif self._model.has_won():#check if the player has won
            messages = [WIN_MESSAGE]
        else:
            return



    def __str__(self) -> str:
        """
        Returns the string representation of the controller.
        Which is the controller description and the file.
        """
        return CONTROLLER_DESC + self._file
    
    def __repr__(self) -> str:
        """
        Returns the representation of the controller.
        Which is the controller description and the file.
        """
        return f"BreachWay({self._file})"


def play_game(file: str) -> None:
    """
    Play the game.
    Check if the file is found,
    if not, print the file not found message.
    Check if the file is malformatted,
    if not, print the malformatted message.
    Play the game.
    """
    try:
        game = BreachWay(file)
    except FileNotFoundError:
        print(f"{file} is not found")
        return
    except ValueError as ve:
        print(f"{file} is malformatted: {ve}")
        return

    game.play()

def main():
    """
    Main function.
    Get the file from the user.
    Play the game.
    """
    file = input("Enter path to level file (e.g. levels/level1.txt): ").strip()
    play_game(file)

if __name__ == "__main__":
    main()

#endregion