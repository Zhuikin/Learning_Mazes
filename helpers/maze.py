from __future__ import annotations
from .grid_cell import GridCell, GridASCIIArt
import json


class Maze:
    """
    Class for static map information
    """

    @classmethod
    def create_from_json(cls, file) -> Maze:
        """ create a map instance from a JSON file
        """
        return cls.deserialize(json.load(file))

    @classmethod
    def deserialize(cls, map_dict) -> Maze:
        """ create a map instance from a dict (as read from JSON)
        """
        gridlist = map_dict["cells"]
        loaded_map = cls(name=map_dict["name"],
                         dim_x=map_dict["dim_x"],
                         dim_y=map_dict["dim_y"])
        loaded_map.start = map_dict["start"]
        loaded_map.goal = map_dict["goal"]

        for cell in gridlist:
            x = cell["x"]
            y = cell["y"]
            loaded_map.make_hole(x, y, cell["hole_chance"])
            if cell["is_blocked"]:
                loaded_map.make_wall(x, y)

        return loaded_map

    def __init__(self, *, name: str, dim_x: int, dim_y: int):
        """ a new map should be created as a new instance using the
            factory (class) methods, rather than calling __init__()
            _dim_x and _dim_y in particular should not be changed at any other
            point otherwise bad things will happen
            the grid is stored at fixed size
        """
        if dim_x < 2 or dim_y < 2:
            raise ValueError("Grid dimensions must be at least 2 x 2")

        self.name = name
        self._dim_x = dim_x
        self._dim_y = dim_y
        self._size = self.dim_x * self._dim_y
        self._start = 0
        self._goal = self.size - 1
        self.grid = tuple(GridCell() for _ in range(self.dim_x * self.dim_y))

    @property
    def dim_x(self) -> int:
        """ maps width / number of columns
        """
        return self._dim_x

    @property
    def dim_y(self) -> int:
        """ maps hieght / number of lines
        """
        return self._dim_y

    @property
    def size(self) -> int:
        """ number of grid cells in the map
        """
        return self._size

    @property
    def start(self) -> tuple[int, int]:
        """ coordinates of the start grid
        """
        return self.unflatten(self._start)

    @start.setter
    def start(self, start: tuple[int, int]):
        x, y = start
        start = self.flatten(x, y)
        if start == self.goal:
            raise ValueError("Collides with goal")
        self.make_floor(x, y)
        self._start = start

    @property
    def goal(self) -> tuple[int, int]:
        """ coordinates of the goal grid
        """
        return self.unflatten(self._goal)

    @goal.setter
    def goal(self, goal: tuple[int, int]):
        x, y = goal
        goal = self.flatten(x, y)
        if goal == self.start:
            raise ValueError("Collides with start")
        self.make_floor(x, y)
        self._goal = goal

    def roll_hole(self, x, y) -> bool:
        """ rolls the hole chance for a given field
        """
        if self.is_start(x, y) or self.is_goal(x, y) or self.is_wall(x, y):
            return False

        if self.get_cell(x, y).is_hole:
            return True

    def flatten(self, x: int, y: int):
        """ for a pair x, y returns a flat index to access (x, y)
            within the grid storage
        """
        if x < 0 or x >= self.dim_x or y < 0 or y >= self.dim_y:
            raise ValueError("Coordinates outside grid dimensions")

        return x + y * self.dim_x

    def unflatten(self, cell_address) -> tuple[int, int]:
        """ retrieves x and y coordinates from a flat cell address
        """
        if cell_address < 0 or cell_address >= self.dim_x * self.dim_y:
            raise ValueError("Cell outside grid dimensions")

        return cell_address % self.dim_x, cell_address // self.dim_x

    def serialize(self) -> dict:
        """ returns a dict for the map instance
            we use that for saving the maps as human-readable JSON
        """
        map_cells = []
        for y in range(self.dim_y):
            for x in range(self.dim_x):
                cell = self.grid[self.flatten(x, y)].serialize()
                cell["x"] = x
                cell["y"] = y
                map_cells.append(cell)
        return {
            "name": self.name,
            "dim_x": self.dim_x,
            "dim_y": self.dim_y,
            "start": self.start,
            "goal": self.goal,
            "cells": map_cells
        }

    def store_json(self, file):
        """ write the calling instance into a JSON file
        """
        json.dump(self.serialize(), file, indent=4)

    def get_cell(self, x: int, y: int) -> GridCell:
        """ for a passed cell (x,y) returns the cell object
        """
        return self.grid[self.flatten(x, y)]

    def is_start(self, x: int, y: int) -> bool:
        """ for a passed cell (x,y) returns True if it's the start cell
        """
        return self.flatten(x, y) == self._start

    def is_goal(self, x: int, y: int) -> bool:
        """ for a passed cell (x,y) returns True if it's the target cell
        """
        return self.flatten(x, y) == self._goal

    def is_wall(self, x: int, y: int) -> bool:
        """ for a given cell (x,y) returns True if the cell is a wall
            all cells outside the grid are considered walls
        """
        if x < 0 or x >= self.dim_x or y < 0 or y >= self.dim_y:
            return True

        return self.grid[self.flatten(x, y)].is_wall

    def can_enter(self, x: int, y: int) -> bool:
        """ check if given cell can be stepped into
        """
        return not self.is_wall(x, y)

    def make_wall(self, x: int, y: int):
        """ marks given cell (x, y) as a blocker
            will refuse (ValueError) to block start or goal
            will override other cell types
        """
        if self.is_goal(x, y) or self.is_start(x, y):
            raise ValueError("Collides with start or goal")

        self.grid[self.flatten(x, y)].is_wall = True

    def make_floor(self, x: int, y: int):
        """ marks the given cell (x, y) as clear floor
            overrides any other floor conditions
        """
        self.grid[self.flatten(x, y)].is_wall = False
        self.grid[self.flatten(x, y)].hole_chance = 0

    def make_hole(self, x: int, y: int, hole_chance: float = 1):
        """ marks the given cell (x, y) as a hole (or assings a chance)
            will refuse (ValueError) to apply holes at start or goal
            overrides other condtions
        """
        if hole_chance > 0 and (self.is_goal(x, y) or self.is_start(x, y)):
            raise ValueError("Collides with start or goal")
        self.grid[self.flatten(x, y)].hole_chance = hole_chance

    def __repr__(self) -> str:
        """ object representation
        """
        return (f"MapGrid(dim_x={self.dim_x}, dim_y={self.dim_y}, "
                f"start={self.start}, goal={self.goal})")

    def ascii_art_buffer(self) -> list[list[str]]:
        """ returns a simple 'ASCII-Art' view of the grid
        """
        artsy_buffer = []
        line_nr = 0
        # frame topside line
        buffer_line = [GridASCIIArt.WALL] * (self.dim_x + 2)
        buffer_line.append(" Y")
        artsy_buffer.append(buffer_line)

        # iteration through the grid, line-wise
        for y in range(self.dim_y):
            buffer_line = [GridASCIIArt.WALL]
            # frame vertical left
            # iteration through the cells in a given line
            for x in range(self.dim_x):
                pixel = self.get_cell(x, y).ascii_art()
                if self.is_start(x, y):
                    pixel = GridASCIIArt.START
                if self.is_goal(x, y):
                    pixel = GridASCIIArt.GOAL
                buffer_line.append(pixel)
            # frame vertical right
            # axis label Y
            buffer_line.append(GridASCIIArt.WALL)
            buffer_line.append(f" {line_nr}")
            line_nr += 1
            artsy_buffer.append(buffer_line)

        # frame line bottom
        buffer_line = [GridASCIIArt.WALL] * (self.dim_x + 2)
        buffer_line.append(" ↓")
        artsy_buffer.append(buffer_line)

        # axis labels X
        buffer_line = [" X "]
        for i in range(self.dim_x):
            buffer_line.append("{:^3}".format(i))
        buffer_line.append("{:^3}".format("→"))
        artsy_buffer.append(buffer_line)

        return artsy_buffer
