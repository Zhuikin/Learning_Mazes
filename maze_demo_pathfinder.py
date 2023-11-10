from maze_agent_access import MazeAgentAccess as Maa
from helpers.maze import Maze
from collections import deque

MAZE_NAME = "Lab_6x6"


def pathfind(grid: Maze,
             horizon, push, pop) -> tuple:
    visited = set()
    nodes_investigated = 0

    # all possible moves
    moves = [(0, 1, "down"),
             (0, -1, "up"),
             (1, 0, "right"),
             (-1, 0, "left")]

    # horizon holds the discovered, but not yet investigated nodes
    while horizon:
        # get a node
        x, y, path = pop()
        nodes_investigated += 1
        if (x, y) not in visited:
            # check if we are done
            if grid.is_goal(x, y):
                return path, nodes_investigated

            # extend the horizon by adding current nodes neighbours
            visited.add((x, y))
            for dx, dy, action in moves:
                new_x, new_y = x + dx, y + dy
                if grid.can_enter(new_x, new_y):
                    push((new_x, new_y, path + [action]))

    # no path if we run out of nodes to check and have not found the goal
    return None, nodes_investigated


def main():
    agent = Maa(name="Eve", maze_foldername=MAZE_NAME)

    print("Loaded maze:")
    agent.print_maze()

    # so we cheat a little and grab the map matrix from the agents interface
    grid = agent.maze
    start_x, start_y = grid.start
    print()

    # run pathfinder as DFS with a stack:
    stack = list()
    stack.append((start_x, start_y, []))
    target_path, steps = pathfind(grid=grid,
                                  horizon=stack,
                                  push=stack.append, pop=stack.pop)
    print(f"Depth First Search path (looked at {steps} nodes):")
    print(target_path)
    # run_path overlays the path sequence over our given map
    string_buffer = agent.trace_path(actions=target_path)
    print(string_buffer)

    # reset
    agent.reset_to_start()
    print()

    # run pathfinder as BFS with a queue:
    queue = deque()
    queue.append((start_x, start_y, []))
    target_path, steps = pathfind(grid=grid,
                                  horizon=queue,
                                  push=queue.append, pop=queue.popleft)
    print(f"Breadth First Search path (looked at {steps} nodes):")
    print(target_path)
    # run_path overlays the path sequence over our given map
    string_buffer = agent.trace_path(actions=target_path)
    print(string_buffer)


if __name__ == "__main__":
    main()
