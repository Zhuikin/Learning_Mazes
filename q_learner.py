from random import random, randint


class QLearner:

    def __init__(self,
                 filename,
                 states: int, actions: int,
                 alpha: float, gamma: float, epsilon: float):

        self.filename = filename
        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qtable = self.make_qtable()

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: int):
        if not 0 <= alpha or alpha > 1:
            raise ValueError("Alpha must be [0:1]")
        self._alpha = alpha

    @property
    def gamma(self) -> int:
        return self._gamma

    @gamma.setter
    def gamma(self, gamma: int):
        if not 0 <= gamma or gamma > 1:
            raise ValueError("Gamma must be [0:1]")
        self._gamma = gamma

    @property
    def epsilon(self) -> int:
        return self._gamma

    @epsilon.setter
    def epsilon(self, epsilon: int):
        if not 0 <= epsilon or epsilon > 1:
            raise ValueError("Gamma must be [0:1]")
        self._epsilon = epsilon

    def update_q(self, s, a, s_next, reward):
        """ update function:
            Q(state, action) =
                (1 - alpha) * Q(s, a) + alpha *
                ( Reward(s, a) + gamma * max Q(s_next, a_next) )
        """
        q_error = reward + self.gamma * max(self.qtable[s_next])
        new_q = (1 - self.alpha) * self.qtable[s][a] + self.alpha * q_error
        self.qtable[s][a] = new_q
        return new_q

    def make_qtable(self):
        """ intialize the QTable with 0 """
        return [[0.0 for _ in range(self.actions)] for _ in range(self.states)]

    def epsilon_greedy_action(self, state) -> int:
        """ pick an action acoording to current policy and table """
        exex_roll = random()

        # run policy (use action with the greater weight in the QTable)
        # we do max "by hand", since pythons max() would always return the
        # first hit, if all are the same
        action_qs = self.qtable[state]
        best_weight = action_qs[0]
        best_action = 0
        all_same = True
        for i in range(1, self.actions):
            if action_qs[i] > best_weight:
                best_weight = action_qs[i]
                best_action = i
                all_same = False

        # if we are not exploring and the action weights are not the same
        if not self.epsilon > exex_roll and not all_same:
            return best_action

        # base case - exploration or the policy not yet determined
        return randint(0, self.actions - 1)
