"""
Interactive demo for the maze interface
Move with WASD
Quit with n

Will only run in a console/shell, not in PYCharms run window
Also needs the console window to be at least (map height + 7) high, or will
throw scary cryptic errors.
Make it at least 20.

requires
pip install windows-curses
"""
from maze_agent_access import MazeAgentAccess
import curses


MAZE_NAME = "FrozenLake_12x10"


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    key = 0

    bob = MazeAgentAccess(name="Bob", maze_foldername=MAZE_NAME)
    still_in_the_hole = False
    while key != ord("n"):

        if bob.is_at_goal:
            # this prints at cursor - line, column
            stdscr.addstr(1, 0, "You found the goal square. Press n to e[n]d")
        # the hole logic needs to keep state until a valid move was taken,
        # to maintain the correct display
        elif bob.is_in_hole or still_in_the_hole:
            stdscr.addstr(1, 0, "Oh noes! We well in. Back to the start.    ")
            still_in_the_hole = True
            bob.reset_to_start()
        else:
            stdscr.addstr(1, 0, "w, a, s, d to move, n to e[n]d             ")

        stdscr.addstr(2, 0, bob.get_maze_view_buffer())
        stdscr.refresh()
        curses.curs_set(0)

        key = stdscr.getch()
        # -1 is returned while the input is empty
        if key != -1:
            # new input was made, reset the hole flag
            if not bob.is_in_hole:
                still_in_the_hole = False
            # resolve moves
            if not bob.is_at_goal and not bob.is_in_hole:
                match chr(key):
                    case "w":
                        bob.step_up()
                    case "s":
                        bob.step_down()
                    case "a":
                        bob.step_left()
                    case "d":
                        bob.step_right()


if __name__ == "__main__":
    try:
        # wrapper does not seem to support with... hence clean up in finally
        curses.wrapper(main)
    except Exception:
        pass
    finally:
        curses.endwin()
