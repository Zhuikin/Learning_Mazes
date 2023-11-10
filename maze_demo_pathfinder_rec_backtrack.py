from maze_agent_access import MazeAgentAccess as Maa
from helpers.maze import Maze

MAZE_NAME = "Lab_12x10"


def backtrack(x: int, y: int, grid: Maze, visited: set):
    """ backtracking is a brute force pathfinder
        it is a recursive-dfs (depth first search)
        this has time complexity of O(number of cells) = O(n**2) for a matrix
        of dimension n
    """
    if grid.is_goal(x, y):
        # recursion base case - no further action needed
        return []

    # visited grids are marked to avoid loops
    visited.add((x, y))

    moves = [(0, 1, "down"),
             (0, -1, "up"),
             (1, 0, "right"),
             (-1, 0, "left")]

    for dx, dy, action in moves:
        new_x, new_y = x + dx, y + dy

        # the recursive call = there will be upto 4 of them through
        # for ... in moves
        if grid.can_enter(new_x, new_y) and (new_x, new_y) not in visited:
            path = backtrack(new_x, new_y, grid, visited)

            # dead ends (never hitting the goal) will come back as None
            if path is not None:
                path.append(action)
                return path

    return None


def main():
    eve = Maa(name="Eve", maze_foldername=MAZE_NAME)

    print("Loaded maze:")
    eve.print_maze()

    # classical pathfinding works on maps, when we can access cells at will,
    # while looking for the correct path
    # the agent based state->action model makes it awkward.
    # so we cheat a little and grab the map from the agents interface
    grid = eve.maze
    visited = set()
    start_x, start_y = grid.start
    print(f"Start: {start_x=}, {start_y=}")

    # the backtracking gives us the path in the reverse order
    # from target back(tracked) to the start
    # reverse() fixes that
    target_path = backtrack(x=start_x, y=start_y, grid=grid, visited=visited)
    target_path.reverse()

    print("Found path:")
    print(target_path)

    # run_path overlays the path sequence over our given map
    string_buffer = eve.trace_path(actions=target_path)
    print(string_buffer)
    if eve.is_at_goal:
        print(f"{eve.name} has found the goal square")
    else:
        print(f"{eve.name} is lost in the dungeon")


if __name__ == "__main__":
    main()
