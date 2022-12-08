import numpy as np

class Trap:
    def __init__(self, spawn_position):
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 10, spawn_position[0] + 25, spawn_position[1] + 40])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
    def move(self,command):
        if command['left_pressed']:
            self.position[0] += 5
            self.position[2] += 5
            
            
        elif command['right_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5