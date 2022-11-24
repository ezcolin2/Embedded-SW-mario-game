from PIL import Image, ImageDraw, ImageFont
import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from Character import Character
from CharacterStop import CharacterStop
from Joystick import Joystick
from Background import Background
from Ground import Ground
from Fire import Fire
from Item import Item

def main():
    x = 0
    background = Image.open("./img/super_map.bmp")
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image)
    # 잔상이 남지 않는 코드 & 대각선 이동 가능
    my_circle = CharacterStop(50,380)
    my_ground = Background((100,100))
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    
    ground1 = Ground((10,150),"normal")
    ground2 = Ground((200,150),"item")
    ground3 = Ground((400,150),"normal")
    grounds = [ground1,ground2,ground3]
    
    realGroundHeight = 140
    fires=[]

    lastDirectionIsLeft=False # 가만히 있어도 최근 방향으로 공격하기 위한 변수 
    fireDelay=0 # 다음 총알을 쏠 때 딜레이 
    
    bullets = []

    item = Item(grounds[1].center) #아이템 생성 처음에는 안 보이게 
    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True
            lastDirectionIsLeft=True
            x-=5

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
            lastDirectionIsLeft=False
            x+=5

        if not joystick.button_B.value: # B pressed
            if fireDelay==0 and my_circle.state=="item":
                fire = Fire(my_circle.center, lastDirectionIsLeft)
                fires.append(fire)
                fireDelay=5
        if(fireDelay>0):
            fireDelay-=1

        if(my_circle.move(command,grounds) and my_circle.state!="item"): # 부딪혔을 때 아직 아이템을 먹지 않은 상황일 때만  item이 보이게
            item.visible=True
        my_ground.move(command)


        
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (124, 255, 255, 100))
        croppedBackground = background.crop(tuple([x,0,240+x,240])).convert("L")
        my_draw.bitmap((0,0),croppedBackground,fill=(242,152,134))
        my_draw.rectangle(tuple(my_ground.position),outline=my_ground.outline,fill=(255,0,0))
        my_draw.ellipse(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
        arrRed=my_circle.arrRed
        arrYellow=my_circle.arrYellow
        arrBrown=my_circle.arrBrown
        size=3
        # if my_circle.right:
        #     for i in arrRed:
        #         print(tuple(i))
        #         my_draw.rectangle((i[0]*size+100,i[1]*size+100+my_circle.position[1],i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(255,0,0,100))
        #     for i in arrYellow:
        #         print(tuple(i))
        #         my_draw.rectangle((i[0]*size+100,i[1]*size+100+my_circle.position[1],i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(255,235,203,100))

        #     for i in arrBrown:
        #         print(tuple(i))
        #         my_draw.rectangle((i[0]*size+100,i[1]*size+100+my_circle.position[1],i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(165,42,42,100))
        # else:
        #     for i in arrRed:
        #         print(tuple(i))
        #         my_draw.rectangle((-i[0]*size+100,i[1]*size+100+my_circle.position[1],-i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(255,0,0,100))
        #     for i in arrYellow:
        #         print(tuple(i))
        #         my_draw.rectangle((-i[0]*size+100,i[1]*size+100+my_circle.position[1],-i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(255,235,203,100))

        #     for i in arrBrown:
        #         print(tuple(i))
        #         my_draw.rectangle((-i[0]*size+100,i[1]*size+100+my_circle.position[1],-i[2]*size+100,i[3]*size+100+my_circle.position[1]),fill=(165,42,42,100))

        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        for i in grounds:
            i.move(command)
            my_draw.rectangle(tuple(i.position),fill = (255,0,0,100))
        

        for i in fires:
            if i.position[2]>240 or i.position[0]<0: #메모리를 아끼기 위해 맵 밖으로 벗어나면 삭제 
                fires.remove(i)
                continue
            i.move(command)
            my_draw.rectangle(tuple(i.position),fill=(255,0,0,100))
        my_circle.isOnItem(item)
        item.move(command)
        if item.visible:
            my_draw.rectangle(tuple(item.position),fill=(124,124,124,100))
        
        joystick.disp.image(my_image)



        

if __name__ == '__main__':
    main()