# TODO
# proper comment formatting
# under the hood:
# move history, update view, stats
from pathlib import Path
from helpers.maze import Maze
from helpers.maze_view import MazeView


def pixel(x: int, y: int, icon=" @ ") -> dict:
    """ helper for creating "pixels" fit to be passed to
        MazeView foreground buffer
        "pixels" are strings of 3 characters, ideally monospace
    """
    return {"x": x, "y": y, "icon": icon}


class InvalidMazeAction(Exception):
    pass


class MazeAgentAccess:

    def __init__(self, name: str, maze_foldername: str):
        """ create a new acent
            maze_foldername is a folder (ex. Lab_4x4, Lab_6x6, ...)

            :raises
                FileNotFoundError if bad maze folder/file is passed
        """
        self.name = name
        self.folder = (Path(__file__).resolve().parent
                       / "mazes" / maze_foldername)

        with open(self.folder / "map.json") as file:
            self.maze = Maze.create_from_json(file)

        self.mv = MazeView(name=f"{self.name} @ {self.maze.name}",
                           maze=self.maze)
        x, y = self.maze.start
        self._pos_x = x
        self._pos_y = y
        self.mv.add_fg_pixel(pixel(x, y))
        self._in_hole = False
        self._in_hole_set_for = (-1, -1)

        self.draw_steps = True
        self.draw_trace = False
        self.step_over_holes = False

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @property
    def states(self) -> int:
        """ this is the number of grid cells in the environment """
        return self.maze.size

    @property
    def actions(self) -> int:
        """ the number of possible actions an agent can take """
        return 4

    @property
    def action_space(self) -> list:
        """ a list of actions an agent take (as method pointers)
            those are ALL possible actions, not the CURRENT valid ones
            this is awkward to use and might be useless.
        """
        return [
            self.step_left,
            self.step_right,
            self.step_up,
            self.step_down
        ]

    def _move(self, to_x: int, to_y: int) -> bool:
        """ move to set location (x, y), if possible
            this is intended for internal use
            for exploration using step_ methods is preferred
        """
        if self.maze.can_enter(to_x, to_y):
            self._pos_x = to_x
            self._pos_y = to_y
            # update holes only if a new grid was entered
            # this is needed in case of probabilistic holes, to avoid
            # re-rolls, unless the state has changes
            if (to_x, to_y) != self._in_hole_set_for:
                self._in_hole = self.maze.roll_hole(to_x, to_y)
                self._in_hole_set_for = (to_x, to_y)
            # live marking of agents position or path/trace
            if self.draw_steps:
                if not self.draw_trace:
                    self.mv.clear_fg()
                self.mv.add_fg_pixel(pixel(to_x, to_y))

            return True

        # in other words if NOT self.maze.can_enter(...)
        else:
            return False

    def get_valid_moves(self) -> list:
        """ get list of all valid moves as method references
            note: the order in the list implies a preference that might
            not suit the algorithm
        """
        moves = []
        if self.can_go_left:
            moves.append(self.step_left)
        if self.can_go_right:
            moves.append(self.step_right)
        if self.can_go_up:
            moves.append(self.step_up)
        if self.can_go_down:
            moves.append(self.step_down)

        return moves

    @property
    def is_at_start(self) -> bool:
        return self.maze.is_start(self.pos_x, self.pos_y)

    @property
    def is_at_goal(self) -> bool:
        return self.maze.is_goal(self.pos_x, self.pos_y)

    @property
    def is_in_hole(self) -> bool:
        return self._in_hole

    @property
    def can_go_left(self) -> bool:
        if not self.step_over_holes and self.is_in_hole:
            return False
        return self.maze.can_enter(self.pos_x - 1, self.pos_y)

    def step_left(self) -> bool:
        """ take a step to the left, if possible"""
        if not self.can_go_left:
            return False
        to_x = self.pos_x - 1
        to_y = self.pos_y
        return self._move(to_x, to_y)

    @property
    def can_go_right(self) -> bool:
        if not self.step_over_holes and self.is_in_hole:
            return False
        return self.maze.can_enter(self.pos_x + 1, self.pos_y)

    def step_right(self) -> bool:
        """ take a step to the left, if possible"""
        if not self.can_go_right:
            return False
        to_x = self.pos_x + 1
        to_y = self.pos_y
        return self._move(to_x, to_y)

    @property
    def can_go_up(self) -> bool:
        if not self.step_over_holes and self.is_in_hole:
            return False
        return self.maze.can_enter(self.pos_x, self.pos_y - 1)

    def step_up(self) -> bool:
        """ take a step to the left, if possible"""
        if not self.can_go_up:
            return False
        to_x = self.pos_x
        to_y = self.pos_y - 1
        return self._move(to_x, to_y)

    @property
    def can_go_down(self) -> bool:
        if not self.step_over_holes and self.is_in_hole:
            return False
        return self.maze.can_enter(self.pos_x, self.pos_y + 1)

    def step_down(self) -> bool:
        """ take a step to the left, if possible"""
        if not self.can_go_down:
            return False
        to_x = self.pos_x
        to_y = self.pos_y + 1
        return self._move(to_x, to_y)

    def reset_to_start(self) -> bool:
        x, y = self.maze.start
        self._in_hole = False
        self._in_hole_set_for = (x, y)
        return self._move(to_x=x, to_y=y)

    def get_maze_view_buffer(self) -> str:
        """ delivers the maze drawing as a string without printing it
        """
        return self.mv.draw_ascii_art()

    # helper methods for printing of results,
    def trace_path(self, actions: list[str],
                   autoreset_on_holes: bool = True,
                   autohalt_on_goal: bool = True) -> str:
        """ runs the sequens of actions as passed and returns
            a representation of the maze with the path marked out
            actions are:
            "left" "right" "up" "down" "reset" (as strings)
            will raise InvalidMazeAction for invalid actions

            :raises
                InvalidMazeAction for bad actions
        """
        if not actions:
            return self.mv.draw_ascii_art()

        old_settings = (self.draw_steps, self.draw_trace)
        self.draw_steps = True
        self.draw_trace = True
        for action in actions:
            match action:
                case "up":
                    self.step_up()
                case "down":
                    self.step_down()
                case "left":
                    self.step_left()
                case "right":
                    self.step_right()
                case "reset":
                    self.reset_to_start()
            if self.is_at_goal and autohalt_on_goal:
                break
            if self.is_in_hole and autoreset_on_holes:
                self.reset_to_start()
        string_buffer = self.mv.draw_ascii_art()
        # restore original draw settings
        self.draw_steps, self.draw_trace = old_settings

        return string_buffer

    def print_maze(self):
        """ prints the state of the maze
        """
        print(self.mv.draw_ascii_art())
