from maze_agent_access import MazeAgentAccess as Maa
from q_learner import QLearner

MAZE_NAME = "Lab_12x10"
# number of training runs. Should be appropriate for the size of the lab
EPISODES = 1000

# reward policy
REWARD_HOLE = -1.0
REWARD_WALL = -0.005
REWARD_GOAL = 1.0
# how many steps can each episode take, as a factor
MAX_STEPS_FACTOR = 5

# meta parameters
ALPHA = 0.5  # learning rate. 1: only believe new info, 0: only old info
GAMMA = 0.5  # temporal discount. 0: only consider current reward
EPSILON = 0.5  # exploration factor. 1: always explore, 0: always run policy


def flatten(x, y, dim_x):
    """ flattens 2 dimensional coordinates into a flat index (state ID)"""
    return x + y * dim_x


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

    # run learning episodes
    for i in range(EPISODES):

        print(f"Episode: {i}")
        qagent.reset_to_start()
        next_episode = False
        for _ in range(max_steps):
            reward = 0
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

    # run the learned policy on the lab
    print("\nLearned QTable:")
    print(ql.qtable)

    print("\nRunning Policy on Lab:")
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
