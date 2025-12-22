from random import random, choice, randint

class QLearning:

    learning_rate = 0.01
    discount_factor = 0.95
    exploration_prob = 0.5
    epochs = 100_000
    actions = [0, 1, 2, 3]

    threshold = 0.05
    
    # states = {"dl": 0, "dr": 0, "dd": 0, "du": 0, 
    #           "dir_up": 0, "dir_down": 0, "dir_left": 0, "dir_right": 0,
    #           "fl": 0, "fr": 0, "fu": 0, "fd": 0}

              # Dangers          Food
    # states = [[0, 0, 0, 0], [0, 0, 0, 0]

    Q = {} # States mapped to actions
     

    
    
    def is_valid(self, action, dir):
        if action == 0 and dir == (-1, 0):
            return False 
        if action == 1 and dir == (0, -1):
            return False 
        if action == 2 and dir == (1, 0):
            return False 
        if action == 3 and dir == (0, 1):
            return False 
        return True
    
    def get_action(self, state, dir):
        if random() < self.exploration_prob:            
            while True:                
                action = choice(self.actions)    
                if self.is_valid(action, dir):
                    break
        else:          
            i = 0         
            while True:
                sorted_actions = sorted(self.Q[state])[::-1]
                max_val = sorted_actions[i]
                action = self.Q[state].index(max_val)
                actions_with_max = [i for i, v in enumerate(self.Q[state]) if v == max_val]
                action = choice(actions_with_max)

                if self.is_valid(action, dir):
                    break                
                i += 1                

                
        return action

    def learn(self, state, action, next_state, reward, done):
        # for epoch in range(self.epochs):        
        # state = tuple(choice((0,1)) for _ in range(8))
        if state not in self.Q: 
            self.Q[state] = [0, 0, 0, 0]       
                   
        # reward = self.step(state, action)
        if next_state not in self.Q:
            self.Q[next_state] = [0, 0, 0, 0]
        
        if done:
            target = reward
        else:
            target = reward + self.discount_factor * max(self.Q[next_state])

        self.Q[state][action] += self.learning_rate * (target - self.Q[state][action])

        # if done:                    
        #     return
                        
                    
        if done:
            self.exploration_prob = max(self.exploration_prob * 0.95, self.threshold)            
            




# for state, action in Q.Q.items():
#     print(state, action)



# from random import random, choice
# from numpy import sqrt, square


# def reward_func(state1, state2):
#     (y1, x1) = state1
#     (y2, x2) = state2
#     y, x = GOAL_STATE
#     dist1 = sqrt(square(x1 - x) + square(y1 - y))
#     dist2 = sqrt(square(x2 - x) + square(y2 - y))

#     if dist2 < dist1:
#         return 0.1
#     return -0.1



# def step(state, action):
#     row, col = state

#     if action == 0 and col < 3:      # right
#         col += 1
#     elif action == 1 and row < 3:    # down
#         row += 1
#     elif action == 2 and col > 0:    # left
#         col -= 1
#     elif action == 3 and row > 0:    # up
#         row -= 1

#     self.next_state = (row, col)    
#     if self.next_state == GOAL_STATE:
#         reward = 1
#         done = True
#     else:
#         reward = reward_func(state, self.next_state)
#         done = False
    
#     return self.next_state, reward, done



# ACTIONS = [0, 1, 2, 3]
# GOAL_STATE = (2, 2)

# Q = {}
# for row in range(4):
#     for col in range(4):
#         Q[(row, col)] = [0, 0, 0, 0]

# learning_rate    = 0.4  # alpha
# discount_factor  = 0.9  # gamma
# exploration_rate = 0.1  # epsilon


# for episode in range(1000):    
#     state = choice(list(Q.keys())) # START HERE

#     while True:
#         if random() < exploration_rate:
#             action = choice(ACTIONS)            
#         else:
#             action = Q[state].index(max(Q[state]))        

#         self.next_state, reward, done = step(state, action) 

#         if done:
#             target = reward
#         else:
#             target = reward + discount_factor * max(Q[self.next_state])

#         Q[state][action] += learning_rate * (target - Q[state][action])
         
#         state = self.next_state
#         if done:
#             break                        
#     exploration_rate = max(0.05, exploration_rate * 0.995)
    
    
# print("Learned Q-table")
# for row in range(4):
#     for col in range(4):
#         d = {0: "höger", 1: "ner", 2: "vänster", 3: "upp"}
#         n = Q[(row, col)].index(max(Q[(row, col)]))
#         print((row, col), d[n], Q[(row, col)])
