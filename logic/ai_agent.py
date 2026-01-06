import random
import numpy as np

class QLearningAgent:
    def __init__(self, maze, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.maze = maze
        self.width = maze.width
        self.height = maze.height
        
        # Q-Table: Key=(x,y), Value=[q_up, q_down, q_left, q_right]
        # Actions: 0: Up, 1: Down, 2: Left, 3: Right
        self.q_table = {}
        
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        self.actions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Up, Down, Left, Right
        
        self.reset()

    def reset(self):
        self.current_pos = self.maze.start
        self.steps = 0
        self.trace = [self.current_pos]

    def get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(4)
        return self.q_table[state]

    def choose_action(self):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3) # Explore
        else:
            state = self.current_pos
            return np.argmax(self.get_q(state)) # Exploit

    def step(self):
        """
        Executes one step of training.
        Returns (done, reward)
        """
        state = self.current_pos
        action_idx = self.choose_action()
        dx, dy = self.actions[action_idx]
        
        nx, ny = state[0] + dx, state[1] + dy
        
        reward = -1 # Living penalty
        done = False
        
        # Check collision or bounds
        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or self.maze.get_cell(nx, ny) == 1:
            # Wall hit
            reward = -10
            next_state = state # Stay in same place
        elif (nx, ny) == self.maze.end:
            # Goal reached
            reward = 100
            done = True
            next_state = (nx, ny)
        else:
            # Valid move
            next_state = (nx, ny)

        # Update Q-Value
        old_q = self.get_q(state)[action_idx]
        next_max_q = np.max(self.get_q(next_state))
        
        new_q = old_q + self.lr * (reward + self.gamma * next_max_q - old_q)
        self.q_table[state][action_idx] = new_q
        
        self.current_pos = next_state
        self.trace.append(self.current_pos)
        self.steps += 1
        
        return done

    def train_episode(self, max_steps=1000):
        self.reset()
        for _ in range(max_steps):
            done = self.step()
            if done:
                break
        return self.trace
