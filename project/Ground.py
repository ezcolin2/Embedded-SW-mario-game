import numpy as np

class Ground:
    def __init__(self, spawn_position, state):
        self.blockState = state # 블록이 일반 블록인지 아이템 블록인지 normal, item
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 15, spawn_position[0] + 25, spawn_position[1] + 15])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
    def move(self,command):
        if command['left_pressed']:
            self.position[0] += 5
            self.position[2] += 5
            
            
        elif command['right_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5
    


    