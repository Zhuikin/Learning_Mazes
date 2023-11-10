import random


class GridASCIIArt:
    """
    Colection of symbols for basic grid drawing in the consol
    """
    WALL = "███"
    FLOOR = "─┼─"
    HOLE = "   "  # "╴┊╶"
    START = " S "
    GOAL = " G "


class GridCell:
    """
    Class to represent grid cells
    """

    def __init__(self, *, is_wall: bool = False, hole_chance: float = 0):
        self.is_wall = is_wall
        self.hole_chance = hole_chance

    @property
    def is_wall(self) -> bool:
        return self._is_blocked

    @is_wall.setter
    def is_wall(self, is_wall: bool):
        """ sets the blocker status of a cell
            will override holes
        """
        if is_wall:
            self._hole_chance = 0
        self._is_blocked = is_wall

    @property
    def is_hole(self) -> bool:
        if self.hole_chance == 0:
            return False
        return random.random() <= self.hole_chance

    @property
    def hole_chance(self) -> float:
        return self._hole_chance

    @hole_chance.setter
    def hole_chance(self, hole_chance: float):
        if hole_chance < 0 or hole_chance > 1:
            raise ValueError("hole_chance should be a probability [0,1]")
        if hole_chance > 0:
            self.is_wall = False
        self._hole_chance = hole_chance

    def serialize(self) -> dict:
        """ returns the current cell as a dict
            we use that to save the maps
        """
        return {"is_blocked": self.is_wall,
                "hole_chance": self.hole_chance}

    def __repr__(self) -> str:
        return (f"GridCell(is_blocked={self.is_wall}, "
                f"is_hole={self.hole_chance})")

    def ascii_art(self, numeric_holes: bool = False) -> str:
        """ returns a simple 'ASCII-Art' view of the cell
        """
        if self.is_wall:
            return GridASCIIArt.WALL
        if self.hole_chance == 0:
            return GridASCIIArt.FLOOR
        else:
            if numeric_holes:
                return f"{self.hole_chance:.1f}"
            else:
                return GridASCIIArt.HOLE
