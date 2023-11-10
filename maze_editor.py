from pathlib import Path
from helpers.maze import Maze
from helpers.maze_view import MazeView

BASE_DIR = Path(__file__).resolve().parent
MAZES_DIR = BASE_DIR / "mazes"


def create() -> str:
    """ create a new empty maze
    """
    print("Creating new maze")
    mazename = input("Name the new maze: ").strip()
    dimensions = input("Maze dimensions (width height): ")
    dimensions = dimensions.split()
    dim_x = int(dimensions[0].strip())
    dim_y = int(dimensions[1].strip())
    maze_dir = MAZES_DIR / mazename
    maze_dir.mkdir()

    maze = Maze(name=mazename, dim_x=dim_x, dim_y=dim_y)
    with open(maze_dir / "map.json", "w") as file:
        maze.store_json(file)
    return mazename


def load() -> str:
    """ selects and a maze folder to read
    """
    while True:
        # get and print directory listing
        maze_folders = [d for d in MAZES_DIR.iterdir() if d.is_dir()]
        print("Mazes:")
        for i in range(len(maze_folders)):
            print("{:<5}{:<70}".format(i, maze_folders[i].name))
        folder = input("Choose folder to load (or (B)ack): ")
        # respond to user quit
        if folder.lower() in ["b", "back"]:
            print("Backing out to menu")
            return ""
        # try choosing folder, repeat until happy or quit
        try:
            folder = int(folder.strip())
        except ValueError:
            print("Could not parse input (expected integer)")
        else:
            if folder < 0 or folder >= len(maze_folders):
                print("Invalid folder choice")
                continue
            return maze_folders[folder].name


def editor(maze: Maze):
    """ basic maze editor to place walls, holes, and more
        start and goal cells
    """
    mv = MazeView(name=f"Editor @ {maze.name}",
                  maze=maze)
    changed = False
    while True:
        # prints current state and explanations
        print(mv.draw_ascii_art())
        print("To edit cells format inputs as follows:\n"
              "wall|floor|start|goal x y | hole x y chance\n"
              "x, y are ints with (0,0) top left, chance is float in [0:1]\n"
              "also (S)ave and quit or (D)iscard edits and quit")
        inputs = input(">>> ").lower().split()
        action = inputs[0].strip()

        # parse cell edits
        if action in ["wall", "floor", "start", "goal", "hole"]:
            try:
                x = int(inputs[1].strip())
                y = int(inputs[2].strip())
                if action == "hole":
                    p = float(inputs[3].strip())
                    maze.make_hole(x, y, p)
            except ValueError as e:
                print(e)
            except IndexError:
                print("Missing parameter(s)")
            else:
                try:
                    match action:
                        case "wall":
                            maze.make_wall(x, y)
                        case "floor":
                            maze.make_floor(x, y)
                        case "start":
                            maze.start = (x, y)
                        case "goal":
                            maze.goal = (x, y)
                except ValueError as e:
                    print(e)
            continue

        # process user commands
        if action in ["s", "save"]:
            maze_file = MAZES_DIR / maze.name / "map.json"
            with open(maze_file, "w") as file:
                maze.store_json(file)
            print("Saved, returning to main menu")
            break
        if action in ["d", "discard"]:
            if changed:
                action = input("Confirm quit without saving with (Y)es: ")
            else:
                action = "y"
            if action.lower() in ["y", "yes"]:
                print("Returning to main menu")
                break
            continue

        print("Input was not understood")


def main():
    maze_name = ""
    while True:

        print(f"\nWorking on: {maze_name if maze_name else 'No maze loaded'}\n"
              f"(C)reate maze template\n"
              f"(L)oad maze for eiting\n"
              f"(Q)uit")

        action = input(">>> ").lower()

        # create and save a maze template
        if action in ["c", "create", "new"]:
            try:
                maze_name = create()
            except ValueError as e:
                print(f"Failed to parse dimensions. {e}")
            except FileExistsError as e:
                print(f"Folder already exists. {e}")
            else:
                print(f"Template saved to {MAZES_DIR / maze_name}")
                maze_name = ""

        # load a maze and switch to display and editor
        if action in ["l", "load"]:
            maze_name = load()
            if maze_name != "":
                with open(MAZES_DIR / maze_name / "map.json", "r") as file:
                    maze = Maze.create_from_json(file)
                editor(maze)

        if action in ["q", "quit"]:
            print("Quitting")
            break


if __name__ == "__main__":
    main()
