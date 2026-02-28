from typing import Optional
from support import *

# Display helper components, you can ignore these until BreachView

class DisplayError(Exception):
    """
    Custom error so as not to trip excepts
    """
    pass

class TextDisplayElement():
    """
    A class to represent and format a block of text content with specified
    dimensions and horizontal/vertical justification. The text content can be
    justified to the top, bottom, or center vertically, and to the left, right,
    or center horizontally.
    """
    VJUST_TOP = "top"
    VJUST_BOTTOM = "bottom"
    VJUST_CENTER = "center" #if unequal sides left
    HJUST_LEFT = "left"
    HJUST_RIGHT = "right"
    HJUST_CENTER = VJUST_CENTER # if unequal sides top
    def __init__(self, 
                 width: Optional[int] = None, 
                 height: Optional[int] = None,
                 vjust: str = VJUST_CENTER,
                 hjust: str = HJUST_CENTER
    ) -> None:
        """
        Initializes a TextDisplayElement with optional fixed width and height,
        and specified vertical and horizontal justification.

        Parameters:
            width (Optional[int]): Fixed width for the text area.
            height (Optional[int]): Fixed height for the text area.
            vjust (str): Vertical justification - must be 'top', 'center',
                or 'bottom'.
            hjust (str): Horizontal justification - must be 'left', 'center',
                or 'right'.
        """
        self._fixwidth = width
        self._fixheight = height

        if vjust not in (self.VJUST_TOP, self.VJUST_CENTER, self.VJUST_BOTTOM):
            raise DisplayError("invalid vertical justification, please use "+ 
                             f"'{self.VJUST_TOP}', " +
                             f"'{self.VJUST_CENTER}', or " +
                             f"'{self.VJUST_BOTTOM}'"
            )
        
        if hjust not in (self.HJUST_LEFT, self.HJUST_CENTER, self.HJUST_RIGHT):
            raise DisplayError("invalid horizontal justification, please use "+ 
                             f"'{self.HJUST_LEFT}', " +
                             f"'{self.HJUST_CENTER}', or " +
                             f"'{self.HJUST_RIGHT}'"
            )
        self._vjust = vjust
        self._hjust = hjust

    def set_width(self, width: Optional[int] = None) -> None:
        """
        Sets a new fixed width for the content display.

        Parameters:
            width (Optional[int]): The desired fixed width.
        """
        self._fixwidth = width

    def get_width(self) -> int:
        """
        Returns the current width of the content area.
        """
        if self._fixwidth:
            return self._fixwidth
        else:
            return max((len(row) for row in self._content), default= 0)
    
    def set_height(self, height: Optional[int] = None):
        """
        Sets a new fixed height for the content display.
        """
        self._fixheight = height

    def get_height(self) -> int:
        """
        Returns the current height of the content area.
        """
        if self._fixheight:
            return self._fixheight
        else:
            return len(self._content)
    
    def justify(self, content: list[str]) -> list[str]:
        """
        Applies horizontal and vertical justification to the provided content.

        Parameters:
            content (list[str]): A list of strings representing the lines of
                text to format.

        Returns:
            list[str]: A list of strings with justified content.
        """
        # pad content horizonally
        to_render = []
        for line in content:
            hdiff = self.get_width() - len(line)
            if hdiff < 0:
                raise DisplayError("Content too wide!")
            if self._hjust == self.HJUST_LEFT:
                to_render.append(line + (" " * hdiff))
            elif self._hjust == self.HJUST_RIGHT:
                to_render.append((" " * hdiff) + line)
            elif self._hjust == self.HJUST_CENTER:
                lpad = hdiff // 2
                rpad = hdiff - lpad
                to_render.append((" " * lpad) + line + (" " * rpad))

        # pad content vertically
        vdiff = self.get_height() - len(to_render)
        if vdiff < 0:
            raise DisplayError("Content too tall!")
        if self._vjust == self.VJUST_TOP:
            to_render += [" " * self.get_width()] * vdiff
        elif self._vjust == self.VJUST_BOTTOM:
            to_render = ([" " * self.get_width()] * vdiff) + to_render
        elif self._vjust == self.VJUST_CENTER:
            tpad = vdiff // 2
            bpad = vdiff - tpad
            to_render = ([" " * self.get_width()] * tpad) + \
                    to_render + \
                    ([" " * self.get_width()] * bpad)
        
        return to_render
        
    def render(self) -> list[str]:
        """
        Returns the internally stored content with justification applied.
        """
        return self.justify(self._content)
    
    def display(self):
        """
        Display the rendered and justified content to the standard output.
        """
        print("\n".join(self.render()))

class BaseDisplay(TextDisplayElement):
    """
    A Display that adds support for setting and wrapping text content on top
    of TextDisplayElement.
    """
    def __init__(self,
                 content: Optional[list[str]] = None, 
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ) -> None:
        """
        Initializes a BaseDisplay object with optional content, dimensions, and
            justification.

        Parameters:
            content (Optional[list[str]]): A list of strings representing
                initial content.
            width (Optional[int]): Fixed width of the display area.
            height (Optional[int]): Fixed height of the display area.
            vjust (str): Vertical justification
            hjust (str): Horizontal justification
        """
        super().__init__(width, height, vjust, hjust)
        self._content = content if content else []

    def set_content(self, content: list[str]):
        """
        Sets or updates the internal content of the display.
        """
        self._content = content

    def wrap_text(self, text: str) -> list[str]:
        """
        Wraps a long string of text into multiple lines based on the current
        width.

        Parameters:
        text (str): The string of text to wrap.

        Returns:
            list[str]: A list of strings where each string fits within the
                display width.
        """
        wrapped = []
        remaining = text
        while len(remaining) > self.get_width():
            # find space to break on
            space = remaining.rfind(" ", 0, self.get_width())
            wrapped.append(remaining[0:space])
            remaining = remaining[space+1:]
            if space == -1:
                break # give up and deal with consequences later

        wrapped.append(remaining)
        return wrapped

class VSplitDisplay(TextDisplayElement):
    """
    A composite display element that stacks multiple TextDisplayElement
    components vertically from top to bottom.
    """
    def __init__(self, 
                 components: list[TextDisplayElement],
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ) -> None:
        """
        Initializes a VSplitDisplay instance with a list of display components
         and optional layout settings.

        Parameters:
            components (list[TextDisplayElement]): The display elements to be
                stacked vertically.
            width (Optional[int]): Fixed width for the overall display.
            height (Optional[int]): Fixed height for the overall display.
            vjust (str): Vertical justification
            hjust (str): Horizontal justification
        """
        super().__init__(width, height, vjust, hjust)
        self._components = components

    def components(self) -> list[TextDisplayElement]:
        """
        Returns the list of child display components.
        """
        return self._components
    
    def __getitem__(self, index: int) -> TextDisplayElement:
        """
        Allows indexed access to the internal list of components.

        Parameters:
            index (int): Index of the component to retrieve.

        Returns:
            TextDisplayElement: The component at the specified index.
        """
        return self._components[index]

    def get_width(self) -> int:
        """
        Returns the width of the VSplitDisplay.
        """
        if self._fixwidth:
            return self._fixwidth
        else:
            return max((component.get_width()
                        for component in self._components), default= 0)
        
    def get_height(self) -> int:
        """
        Returns the height of the VSplitDisplay.
        """
        if self._fixheight:
            return self._fixheight
        else:
            return sum((component.get_height()
                        for component in self._components))

    def render(self):
        """
        Renders all components and stacks their output vertically into a
            single list of lines.
        """
        content_stack = []
        for component in self._components:
            content_stack += component.render()
        return self.justify(content_stack)

class HSplitDisplay(TextDisplayElement):
    """
    A composite display element that arranges multiple TextDisplayElement
    components horizontally from left to right.
    """
    def __init__(self, 
                 components: list[TextDisplayElement],
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ) -> None:
        """
        Initializes an HSplitDisplay with the given components and optional
        layout settings.

        Parameters:
            components (list[TextDisplayElement]): The display elements to be
                arranged horizontally.
            width (Optional[int]): Fixed total width of the display.
            height (Optional[int]): Fixed total height of the display.
            vjust (str): Vertical justification
            hjust (str): Horizontal justification
        """
        super().__init__(width, height, vjust, hjust)
        self._components = components

    def components(self) -> list[TextDisplayElement]:
        """
        Returns the list of child display components.
        """
        return self._components
    
    def __getitem__(self, index: int) -> TextDisplayElement:
        """
        Allows indexed access to the internal list of components.

        Parameters:
            index (int): Index of the component to retrieve.

        Returns:
            TextDisplayElement: The component at the specified index.
        """
        return self._components[index]
    
    def get_width(self) -> int:
        """
                Returns the width of the VSplitDisplay.
                """
        if self._fixwidth:
            return self._fixwidth
        else:
            return sum((component.get_width()
                        for component in self._components))
        
    def get_height(self) -> int:
        """
        Returns the height of the VSplitDisplay.
        """
        if self._fixheight:
            return self._fixheight
        else:
            return max((component.get_height()
                        for component in self._components), default= 0)

    def render(self):
        """
        Renders all components and stacks their output vertically into a
            single list of lines.
        """
        to_render = ["" for _ in range(self.get_height())]

        for component in self._components:
            new_content = component.render()
            # will need to pad vertically early
            vdiff = self.get_height() - len(new_content)
            if vdiff < 0:
                raise DisplayError("Component is too tall!")
            if self._vjust == self.VJUST_TOP:
                new_content += [" " * component.get_width()] * vdiff
            elif self._vjust == self.VJUST_BOTTOM:
                new_content = ([" " * component.get_width()] * vdiff
                               + new_content)
            elif self._vjust == self.VJUST_CENTER:
                tpad = vdiff // 2
                bpad = vdiff - tpad
                new_content = [" " * component.get_width()] * tpad + \
                        new_content + \
                        [" " * component.get_width()] * bpad
            
            #stitch lines together
            for line in range(self.get_height()):
                to_render[line] += new_content[line]

        return self.justify(to_render)

class AbstractGrid(VSplitDisplay):
    """
    A display element that arranges components in a fixed-size grid layout.

    The grid is composed of rows and columns, where each cell is a display
    element with calculated or enforced dimensions. Supports two layout modes:
        - 'square': each cell has equal width and height
        - 'stretch': each cell stretches to fill available space
    """
    GRID_SQUARE = "square"
    GRID_STRETCH = "stretch"
    _FIXED_GEO_ERR = DisplayError("Grid must have fixed geometry")
    def __init__(self, 
                 dims: tuple[int, int], #row col
                 width: int, 
                 height: int, 
                 just: str = GRID_SQUARE
    ) -> None:
        """
        Initializes an AbstractGrid with fixed dimensions and layout mode.

        Parameters:
            dims (tuple[int, int]): Number of rows and columns in the grid.
            width (int): Total width of the grid.
            height (int): Total height of the grid.
            just (str): Layout mode, either 'square' or 'stretch'.
        """
        if not width and height:
            raise self._FIXED_GEO_ERR
        
        super().__init__([], width, height)
        
        if just not in (self.GRID_SQUARE, self.GRID_STRETCH):
            raise DisplayError("invalid grid justification, please use "+ 
                             f"'{self.GRID_SQUARE}', or" +
                             f"'{self.GRID_STRETCH}'"
            )
        self._grid_just = just
        self.set_dims(dims)

    def set_width(self, width: int):
        """
        Sets a new fixed width for the grid.
        """
        if not width:
            raise self._FIXED_GEO_ERR
        super().set_width(width)
        self.set_dims(self._dims) # Reconstruct grid with new geometry
    
    def set_height(self, height: int):
        """
        Sets a new fixed height for the grid.
        """
        if not height:
            raise self._FIXED_GEO_ERR
        super().set_height(height)
        self.set_dims(self._dims) # Reconstruct grid with new geometry

    def get_dims(self) -> tuple[int, int]:
        """
        Returns the current dimensions of the grid.
        """
        return self._dims

    def set_dims(self, dims: tuple[int, int]) -> None:
        """
        Sets new grid dimensions and rebuilds the grid cells accordingly.
        """
        self._dims = dims

        # Determine cell dims
        cell_height = self._fixheight // dims[0]
        cell_width = self._fixwidth // dims[1]

        self.components().clear()
        for _ in range(dims[0]):
            if self._grid_just == self.GRID_SQUARE:
                min_dim = min(cell_height, cell_width)
                cell_height = min_dim
                cell_width = min_dim

            row_components = [BaseDisplay(width=cell_width, height=cell_height)
                              for _ in range(dims[1])]
            self.components().append(HSplitDisplay(row_components, 
                                                   width=self.get_width(), 
                                                   height = cell_height)
            )

    def get_cell(self, row: int, col: int):
        """
        Returns the display element at a specific cell in the grid.
        """
        return self[row][col]

BREACH_WIDTH = 80
DIVIDER = "-" * BREACH_WIDTH
TITLE = "BreachWay"

HARD_POINT_DISPLAY = "O"
LL_DISPLAY = "@"
HL_DISPLAY = "o"
SG_DISPLAY = "*"
DESTROYED_DISPLAY = "X"
RECHARGING_DISPLAY = "+"

class ShipDisplay(AbstractGrid):
    """
    A visual representation of a ship composed of hardpoints and fixed ship
    components.
    """
    NOSE = [" ^ ","/ \\","|-|"]
    LFIN = ["  /", " / ", "/M-"]
    RFIN = ["\\  ", " \\ ", "-M\\"]
    BASE = ["| |", "|^|", "M|M"]

    SHIP_CELL_SIZE = 3
    SHIP_CELLS_WIDE = 3

    DISPLAY_MAP = {
        HARD_POINT_SYMBOL: HARD_POINT_DISPLAY,
        LL_SYMBOL: LL_DISPLAY,
        HL_SYMBOL: HL_DISPLAY,
        SG_SYMBOL: SG_DISPLAY,
        RECHARGING_SYMBOL: RECHARGING_DISPLAY
    }

    def __init__(self, hardpoints: list["Hardpoint"] = None) -> None:
        """
        Initializes a ShipDisplay with optional hardpoint data.

        Parameters:
            hardpoints (list[Hardpoint]): A list of Hardpoint objects to be
                displayed.
        """
        super().__init__((1,3), width = self.SHIP_CELL_SIZE *
                                        self.SHIP_CELLS_WIDE, height=1)
        if hardpoints:
            self.set_ship(hardpoints)

    def set_ship(self, hardpoints = list["Hardpoint"]) -> None:
        """
        Configures the ship display with the given hardpoints.
        """
        # Set dims and geometry
        self.set_dims((len(hardpoints)+2, self.SHIP_CELLS_WIDE))
        self.set_height(self.SHIP_CELL_SIZE * (len(hardpoints)+2))

        # Draw fixed ends
        self[0][1].set_content(self.NOSE)
        self[-1][0].set_content(self.LFIN)
        self[-1][1].set_content(self.BASE)
        self[-1][2].set_content(self.RFIN)

        # Draw hardpoints
        for i, hardpoint in enumerate(hardpoints):
            pos = i+1
            if hardpoint.is_functional():
                display = self.DISPLAY_MAP[str(hardpoint)]
            else: 
                display = DESTROYED_DISPLAY
            # Hardpoint + health
            self[pos][1].set_content(
                    ["| |",f"|{display}|",f"|{hardpoint.get_armour()}|"]
            )
            # Position
            self[pos][0].set_content(f"{pos}")

class StatBar(HSplitDisplay):
    """
    A horizontal bar display for showing player and enemy ship statistics.
    """
    STAT_HEIGHT = 2
    REACTOR_STRING = "Reactor Energy Available"
    def __init__(self, width: int) -> None:
        """
        Initializes the stat bar layout with the specified width.

        Parameters:
            width (int): The total width of the stat bar display.
        """
        super().__init__(
            [
                BaseDisplay(
                    width = ShipDisplay.SHIP_CELLS_WIDE
                            * ShipDisplay.SHIP_CELL_SIZE,
                    height = self.STAT_HEIGHT, 
                    vjust = TextDisplayElement.VJUST_BOTTOM,
                ),
                BaseDisplay(
                    ["|"] * self.STAT_HEIGHT,
                    width = 1,
                    height = self.STAT_HEIGHT,
                ),
                BaseDisplay(
                    width = ShipDisplay.SHIP_CELLS_WIDE
                            * ShipDisplay.SHIP_CELL_SIZE,
                    height = self.STAT_HEIGHT, 
                    vjust = TextDisplayElement.VJUST_BOTTOM
                ),
                BaseDisplay(
                    height = self.STAT_HEIGHT,
                    width =  width - (2*(ShipDisplay.SHIP_CELLS_WIDE
                                         * ShipDisplay.SHIP_CELL_SIZE) +1),
                    vjust = TextDisplayElement.VJUST_BOTTOM,
                    hjust = TextDisplayElement.HJUST_RIGHT
                ),
            ],
            width=width, 
            height=self.STAT_HEIGHT, 
            vjust = TextDisplayElement.VJUST_BOTTOM,
            hjust=TextDisplayElement.HJUST_LEFT,
        )
    
    def display_stats(
            self, 
            player_armour: int, 
            player_shield: int,
            player_heat: int, 
            player_energy: int, 
            enemy_armour: int, 
            enemy_shield: int, 
            enemy_heat: int
        ) -> None:
        """
        Populates the stat bar with values for both the player and the enemy,
        and displays the player's available reactor energy.

        Parameters:
            player_armour (int): Player ship's current armour value.
            player_shield (int): Player ship's current shield value.
            player_heat (int): Player ship's current heat level.
            player_energy (int): Energy available from the player's reactor.
            enemy_armour (int): Enemy ship's current armour value.
            enemy_shield (int): Enemy ship's current shield value.
            enemy_heat (int): Enemy ship's current heat level.
        """

        # Display Player ship stats:
        self[0].set_content([
            f"A:{player_armour}", 
            f"S:{player_shield} H:{player_heat}"])
        
        # Display enemy ship stats:
        self[2].set_content([
            f"A:{enemy_armour}", 
            f"S:{enemy_shield} H:{enemy_heat}"])
        
        # Display energy
        self[3].set_content([
            self.REACTOR_STRING, str(player_energy)
        ])

class EncounterDisplay(VSplitDisplay):
    """
    Displays the full combat encounter UI including player and enemy ships,
    a vertical divider, enemy intents, and combat statistics.
    """
    
    def __init__(self, width: int) -> None:
        """
        Initializes the encounter layout with a given width.

        Parameters:
            width (int): The full width of the encounter display area.

        """
        ships = HSplitDisplay(
            [ShipDisplay(), BaseDisplay(), ShipDisplay(), VSplitDisplay([])],
            width=width, vjust = TextDisplayElement.VJUST_BOTTOM,
            hjust= TextDisplayElement.HJUST_LEFT
        )
        stats = StatBar(width)
        super().__init__([ships,BaseDisplay([DIVIDER]),stats],
            width = width, vjust = TextDisplayElement.VJUST_BOTTOM)
        
    def display_ships(self, player: "Ship", enemy: "Ship"):
        """
        Updates the display with information from the given player and enemy
        ships.

        Parameters:
            player (Ship): The player's ship instance.
            enemy (Ship): The enemy's ship instance.
        """
        # Display player
        self[0][0].set_ship(player.get_hardpoints())

        # Display enemy with intents
        e_intents = enemy.get_intents()
        self[0][2].set_ship([intent[0] for intent in e_intents])
        self[0][3].components().clear()
        # Buffer for nose cone
        self[0][3].components().append(
            BaseDisplay(height=ShipDisplay.SHIP_CELL_SIZE))

        for intent in e_intents:
            self[0][3].components().append(
                BaseDisplay(
                    [intent[1]], height=ShipDisplay.SHIP_CELL_SIZE
                )
            )
        self[0][3].components().append(
            BaseDisplay(height=ShipDisplay.SHIP_CELL_SIZE)) # Buffer for Base

        # Display Divider
        self[0][1].set_content([]) # to not mess with get_height
        self[0][1].set_content(["|"]* self.get_height())

        # Display stats
        self[2].display_stats(
            player.get_armour(),
            player.get_shield(),
            player.get_heat(),
            player.get_energy(),
            enemy.get_armour(),
            enemy.get_shield(),
            enemy.get_heat()
        )

class CardDisplay(VSplitDisplay):
    """
    A visual representation of a card with borders, number identifier,
    and internal content such as name, description, cost, and cooldown.
    """
    CARD_WIDTH = 12
    CARD_HEIGHT = 10
    CARD_HBORDER = ["+" + ("-" * CARD_WIDTH) + "+"]
    CARD_VBORDER = ["|"] * CARD_HEIGHT

    def __init__(self, padding: int) -> None:
        """
        Initializes the bordered card layout.

        Parameters:
            padding (int): Extra horizontal padding added to the right of the
                card for layout alignment.
        """
        super().__init__([
            BaseDisplay(
                [], 
                width = self.CARD_WIDTH + 2,
                height = 1    
            ),
            BaseDisplay(
                self.CARD_HBORDER, 
                width = self.CARD_WIDTH + 2,
                height = 1    
            ),
            HSplitDisplay([
                BaseDisplay(
                    self.CARD_VBORDER, 
                    width = 1,
                    height = self.CARD_HEIGHT   
                ),
                BaseDisplay(
                    width = self.CARD_WIDTH, 
                    height=self.CARD_HEIGHT,
                    vjust= CardDisplay.VJUST_TOP
                ),
                BaseDisplay(
                    self.CARD_VBORDER, 
                    width = 1,
                    height = self.CARD_HEIGHT   
                )  
            ]),
            BaseDisplay(
                self.CARD_HBORDER, 
                width = self.CARD_WIDTH + 2,
                height = 1    
            )
        ], 
        width = self.CARD_WIDTH + 2 + padding, 
        height = self.CARD_HEIGHT + 3
        )
        
    def set_card(self, card: "Card", num: int):
        """
        Populates the card display with content from a given Card object.

        Parameters:
            card (Card): The card object to render.
            num (int): The numeric identifier for the card.
        """
        # Adjust displayed number
        self[0].set_content([str(num)])

        # split name and desc
        text = str(card)
        split = text.split(": ")
        if len(split)> 1:
            name = split[0]
            desc = ": ".join(split[1:])
        else: #fallback in case students throw custom stuff in
            name = ""
            desc = text
        
        content = [name,""]
        content.extend(self[2][1].wrap_text(desc))
        
        # Add stats to end
        content.append("")
        content.append(f"Cost: {card.get_cost()}")
        content.append(f"Cooldown: {card.get_cooldown()}")

        self[2][1].set_content(content)
    
class HandDisplay(HSplitDisplay):
    """
        A horizontal layout for displaying a player's hand of cards.
    """
    V_BUFFER = 5
    def __init__(self, width: int = None) -> None:
        """
        Initializes an empty hand display area.

        Parameters:
            width (int, optional): Total width of the hand display.
        """
        super().__init__(
            [], width=width, height = CardDisplay.CARD_HEIGHT + self.V_BUFFER
        )
    
    def display_hand(self, hand: list["Card"]) -> None:
        """
        Populates the hand display with a list of card objects.

        Parameters:
            hand (list[Card]): The list of cards to be displayed.
        """
        self.components().clear()
        padding = (self.get_width() -
                   ((CardDisplay.CARD_WIDTH+2) * len(hand))) // len(hand)

        for i, card in enumerate(hand):
            card_display = CardDisplay(padding)
            card_display.set_card(card, i+1)
            self.components().append(card_display)

class BreachView(VSplitDisplay):
    """
    View class that displays Breachway game state with structured prints.
    """
    def __init__(self):
        """
        Initialises a new BreachView.
        """
        header = BaseDisplay([DIVIDER, TITLE, DIVIDER], width = BREACH_WIDTH)
        encounter = EncounterDisplay(BREACH_WIDTH)
        hand = HandDisplay(BREACH_WIDTH)
        message_bar = BaseDisplay([DIVIDER, DIVIDER], width = BREACH_WIDTH)

        super().__init__(
            [header,encounter,hand,message_bar], 
            width=BREACH_WIDTH, 
            vjust=BaseDisplay.VJUST_BOTTOM
        )

    def display_game(self, 
                     player: "Player", 
                     opponent: "Enemy", 
                     cards: list["Card"], 
                     messages: list[str]
        ):
        """
        Updates the game display by making a new structured print.

        Args:
            player (Player): Player ship to display.
            opponent (Enemy): Active enemy to display.
            cards (list[Card]): Players current hand.
            messages (list[str]): Messages to communicate to the player. 
                                  Will be automatically wrapped as neccessary.
                                  Messages appear in order, with the first 
                                  message in the list appearing topmost, 
                                  and the last message in the list appearing
                                    bottommost.
        """
        self[1].display_ships(player, opponent) # Encounter
        self[2].display_hand(cards) # Hand
        # Wrap messages:
        wrapped = []
        for message in messages:
            wrapped += self[3].wrap_text(message)
        self[3].set_content([DIVIDER] + wrapped + [DIVIDER]) # Message Bar
        self.display()