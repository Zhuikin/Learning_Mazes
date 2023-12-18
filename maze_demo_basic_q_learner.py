from maze_agent_access import MazeAgentAccess as Maa
from q_learner import QLearner
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np

# MAZE_NAME = "Lab_12x10"
# MAZE_NAME = "FrozenLake_5x5"
MAZE_NAME = "FrozenLake_12x10"
# number of training runs. Should be appropriate for the size of the lab
EPISODES = 1000
# how many steps can each episode take, as a factor
MAX_STEPS_FACTOR = 10

# reward policy
REWARD_HOLE = -1.0
REWARD_WALL = -0.75
REWARD_GOAL = 2.0
REWARD_STEP = -0.1


# meta parameters
ALPHA = 0.5  # learning rate. 1: only believe new info, 0: only old info
GAMMA = 0.5  # temporal discount. 0: only consider current reward
EPSILON = 0.5  # exploration factor. 1: always explore, 0: always run policy


def flatten(x, y, dim_x):
    """ flattens 2 dimensional coordinates into a flat index (state ID)"""
    return x + y * dim_x


def visualize_qtable(dim_x, dim_y, qtable):
    """ reforamts the q-table to get a map like representation. 
        this is specific to this demo, since the mapping of states and actions
        depends on the setting. 
    """
    # actions order: left, right, up, down
    value_map = [[0.0 for _ in range(dim_x)] for _ in range(dim_y)]
    count_map = [[0 for _ in range(dim_x)] for _ in range(dim_y)]

    for i in range(dim_x):
        for j in range(dim_y):

            if(i-1) >= 0:
                value_map[j][i-1] += qtable[flatten(i, j, dim_x)][0]
                count_map[j][i-1] += 1
            if(i+1) < dim_x:
                value_map[j][i+1] += qtable[flatten(i, j, dim_x)][1]
                count_map[j][i+1] += 1
            if(j-1) >= 0:
                value_map[j-1][i] += qtable[flatten(i, j, dim_x)][2]
                count_map[j-1][i] += 1
            if(j+1) < dim_y:
                value_map[j+1][i] += qtable[flatten(i, j, dim_x)][3]
                count_map[j+1][i] += 1 

    for i in range(dim_y):
        for j in range(dim_x):
            value_map[i][j] = value_map[i][j] / count_map[i][j]


    return value_map


def main():
    # initialize everything
    qagent = Maa(name="Quinn", maze_foldername=MAZE_NAME)
    dim_x = qagent.maze.dim_x
    dim_y = qagent.maze.dim_y
    states = dim_x * dim_y
    max_steps = states * MAX_STEPS_FACTOR
    actions = qagent.action_space
    ql = QLearner(filename="not set",
                  states=states,
                  actions=len(actions),
                  alpha=ALPHA,
                  gamma=GAMMA,
                  epsilon=EPSILON
                  )

    print("\nLoaded maze:")
    print(qagent.get_maze_view_buffer())
    # run learning episodes
    for i in range(EPISODES):

        # print(f"Episode: {i}")
        qagent.reset_to_start()
        next_episode = False
        for _ in range(max_steps):
            reward = REWARD_STEP
            # get current state and choose action
            state = flatten(qagent.pos_x, qagent.pos_y, dim_x)
            action = ql.epsilon_greedy_action(state)
            # action_fn is a method pointer to one of the move methods
            action_fn = actions[action]
            state_changed = action_fn()

            if not state_changed:
                reward = REWARD_WALL
            if qagent.is_at_goal:
                reward = REWARD_GOAL
                next_episode = True
            if qagent.is_in_hole:
                reward = REWARD_HOLE
                next_episode = True

            # get new state and update the Q Table
            new_state = flatten(qagent.pos_x, qagent.pos_y, dim_x)
            ql.update_q(
                s=state,
                a=action,
                s_next=new_state,
                reward=reward
            )

            if next_episode:
                break

    # show a representation of the learned map
    print("\nLearned map from QTable:")
    v_map = visualize_qtable(dim_x, dim_y, ql.qtable)
    matrix = np.array(v_map)
    cmap = plt.get_cmap("RdYlGn")
    plt.imshow(matrix, cmap=cmap, interpolation="nearest", aspect="auto")
    plt.colorbar()
    plt.title("Rewards map")
    plt.show()


    # run the learned policy on the lab
    print("\nRunning Policy on Lab:")
    # qagent.maze.start=(4,4)
    qagent.reset_to_start()
    ql.epsilon = 0
    qagent.draw_trace = True


    while not qagent.is_at_goal:
        state = flatten(qagent.pos_x, qagent.pos_y, dim_x)
        action_fn = actions[ql.epsilon_greedy_action(state)]
        action_fn()
        if qagent.is_in_hole:
            qagent.reset_to_start()

    string_buffer = qagent.get_maze_view_buffer()
    print(string_buffer)


if __name__ == "__main__":
    main()
