import numpy as np

class Background:
    def __init__(self,spawn_position):
        self.appearance = 'rectangle'
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 25, spawn_position[0] + 25, spawn_position[1] + 25])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#00FF00"
    def move(self, command = None):
        self.outline = "#FF0000" #빨강색상 코드!


        if command['left_pressed']:
            self.position[0] += 5
            self.position[2] += 5
            
        elif command['right_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5