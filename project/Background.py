import numpy as np

class Background:
    def __init__(self,spawn_position):
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 25, spawn_position[0] + 25, spawn_position[1] + 25])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
    def move(self, command = None):


        if command['left_pressed']:
            self.position[0] += 5
            self.position[2] += 5
            
        elif command['right_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5