
import numpy as np

class Item:
    def __init__(self, spawn_position):
        #spawn_position은 ground의 center 값을 받고 ground보다 살짝 위로 Item 좌표 설정 
        self.position = np.array([spawn_position[0] - 5, spawn_position[1] - 20, spawn_position[0] + 5, spawn_position[1] + -10])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

        self.visible = False
    def move(self,command):
        if command['left_pressed']:
            self.position[0] += 5
            self.position[2] += 5
            
            
        elif command['right_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5
    
