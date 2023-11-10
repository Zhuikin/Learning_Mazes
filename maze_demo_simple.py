from maze_agent_access import MazeAgentAccess

MAZE_NAME = "Lab_6x6"


def main():
    """ simple demo running a predefined path """

    alice = MazeAgentAccess(name="Alice", maze_foldername=MAZE_NAME)

    print("Loaded maze:")
    alice.print_maze()

    path = ["up", "right", "right", "down", "right",
            "right", "down", "right", "down", "down"]

    print("Running path:")
    print(path)
    string_buffer = alice.trace_path(actions=path)

    print(string_buffer)

    if alice.is_at_goal:
        print("Alice has found the goal square")
    else:
        print("Alice is lost in the labyrinth")


if __name__ == "__main__":
    main()
