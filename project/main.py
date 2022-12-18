from PIL import Image, ImageDraw, ImageFont
import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from  Mario import Mario 
from Joystick import Joystick
from Background import Background
from Ground import Ground
from Fire import Fire
from Item import Item
from Monster import Monster
from Trap import Trap
from Coin import Coin
from Boss import Boss
from Stone import Stone
from time import sleep
life = 3

def main():
    global life
    isWin = False #승리했는지 알려줌 
    font = ImageFont.truetype("./font/mario.ttf",20)
    itemFont = ImageFont.truetype("./font/mario.ttf",30)
    score = 0 # 점수
    x = 0
    start = Image.open("./img/start.png")
    background = Image.open('./img/map.bmp').convert('L')
    endingImg = Image.open('./img/ending.png')
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    while(life==3 or life==0):
        joystick.disp.image(start)
        if not joystick.button_A.value:
            break
    joystick.disp.image(my_image)
    # 잔상이 남지 않는 코드 & 대각선 이동 가능
    mario = Mario(100,380)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    
    ground1 = Ground((300,150),"coin")
    ground2 = Ground((330,150),"normal")
    ground7 = Ground((330,80),"coin")
    ground3 = Ground((360,150),"coin")

    ground4 = Ground((630,150),"normal")
    ground5 = Ground((700,150),"normal")
    ground6 = Ground((750,80),"item")
    ground8 = Ground((1530,150),"coin")
    ground9 = Ground((1560,150),"coin")
    ground10 = Ground((1590,150),"coin")
    grounds = [ground1,ground2,ground3,ground4,ground5,ground6,ground7,ground8,ground9,ground10]

    monster1 = Monster((200,200))
    monster2 = Monster((350,200))
    monster3 = Monster((300,200))
    monster4 = Monster((1000,200))
    monster5 = Monster((1200,200))
    monster6 = Monster((1300,200))
    monsters = [monster1, monster2, monster3, monster4, monster5, monster6]

    boss = Boss((2000,200))

    stone1 = Stone((1900,0))
    stone2 = Stone((1820,0))
    stone3 = Stone((1740,0))
    stones = [stone1,stone2,stone3]

    trap1 = Trap((600,220))
    trap2 = Trap((650,220))
    trap3 = Trap((700,220))
    trap4 = Trap((750,220))
    trap5 = Trap((800,220))
    trap6 = Trap((850,220))
    traps = [trap1,trap2,trap3,trap4,trap5,trap6]
    realGroundHeight = 140
    fires=[]

    lastDirectionIsLeft=False # 가만히 있어도 최근 방향으로 공격하기 위한 변수 
    fireDelay=0 # 다음 총알을 쏠 때 딜레이 
    
    bullets = []

    item = Item(ground6.center) #아이템 생성 처음에는 안 보이게 

    coin1 = Coin(ground1.center) #코인 생성 처음에는 안 보이게 
    coin2 = Coin(ground3.center) #코인 생성 처음에는 안 보이게 
    coin3 = Coin(ground7.center) #코인 생성 처음에는 안 보이게 
    coin4 = Coin(ground8.center) #코인 생성 처음에는 안 보이게 
    coin5 = Coin(ground9.center) #코인 생성 처음에는 안 보이게 
    coin6 = Coin(ground10.center) #코인 생성 처음에는 안 보이게 
    coins  = [coin1,coin2,coin3,coin4,coin5,coin6]
    while True:
        command = {'move': False, 'up_pressed': 
        False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'a_pressed' : False}
       
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
        if not joystick.button_A.value: # B pressed
            command['a_pressed'] = True
        if not joystick.button_B.value: # B pressed
            if fireDelay==0 and mario.state=="item":
                fire = Fire(mario.center, lastDirectionIsLeft)
                fires.append(fire)
                fireDelay=5
        if(fireDelay>0):
            fireDelay-=1

        isItemOrCoin = mario.move(command,grounds)
        if isItemOrCoin!=None:
            if isItemOrCoin[0]=="item": # 부딪혔을 때 아직 아이템을 먹지 않은 상황일 때만  item이 보이게
                if mario.state!="item":
                    item.visible=True

            elif isItemOrCoin[0] == "coin" : # 코인 벽돌에 부딪힌 것을 알음 
                for i in coins: # 어느 코인에 부딪혔는지 알기 위해 부딪힌 블록의 중앙값을 반환받음 중앙값의 x좌표가 동일한 코인을 찾는다 
                    if i.center[0]==isItemOrCoin[1][0]:
                        i.visible=True




        
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (124, 255, 255, 25))
        croppedBackground = background.crop(tuple([x,0,240+x,240]))
        my_draw.bitmap((0,0),croppedBackground,fill=(242,152,134))
        arrRed=mario.arrRed
        arrYellow=mario.arrYellow
        arrBrown=mario.arrBrown

        
        for i in traps:
            mario.onTrap(i)
            i.move(command)
            my_draw.rectangle(tuple(i.position),fill=(255,0,0))
        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        for i in grounds:
            i.move(command)
            if i.blockState=="coin":
                my_draw.rectangle(tuple(i.position),fill = (255,215,0,100))
            else:
                my_draw.rectangle(tuple(i.position),fill = (255,127,0,100))
            my_draw.rectangle((i.position[0],i.position[1]-5,i.position[2],i.position[1]),fill=(235,221,204,100))
            if i.blockState=="item":
                my_draw.text((i.position[0]+15,i.position[1]),'?',font=itemFont)

        for i in fires:
            if i.hitBoss(boss):
                fires.remove(i)
            elif i.hit(monsters):#적과 닿으면 적과 공격을 없앰 
                fires.remove(i)
            elif i.position[2]>240 or i.position[0]<0: #메모리를 아끼기 위해 맵 밖으로 벗어나면 삭제 
                fires.remove(i)
                continue
            i.move(command)
            my_draw.rectangle(tuple(i.position),fill=(255,0,0,100))
        mario.isOnItem(item)
        item.move(command)
        if item.visible:
            my_draw.rectangle(tuple(item.position),fill=(124,124,124,100))

        for i in coins:
            if mario.isOnCoin(i,command) : # 동전에 닿은 상태에서 A를 눌러야 함 
                score+=5
            i.move(command)
            if i.visible:
                my_draw.ellipse(tuple(i.position),fill=(255,215,0,100),outline="#D6B534")


        for i in monsters:
            mario.monsterHitted(i)
            if i.state=='dead':
                monsters.remove(i)
            if i.state=='alive': #살이있을 때만 

                i.move(command)
                for j in i.arrBrown:
                    my_draw.rectangle((i.direction*j[0]*i.size+i.position[2]-25,j[1]*i.size+200,i.direction*j[2]*i.size+i.position[2]-25,j[3]*i.size+200),fill=(150,75,0,100))
                for j in i.arrBlack:
                    my_draw.rectangle((i.direction*j[0]*i.size+i.position[2]-25,j[1]*i.size+200,i.direction*j[2]*i.size+i.position[2]-25,j[3]*i.size+200),fill=(0,0,0,100))

                for j in i.arrWhite:
                    my_draw.rectangle((i.direction*j[0]*i.size+i.position[2]-25,j[1]*i.size+200,i.direction*j[2]*i.size+i.position[2]-25,j[3]*i.size+200),fill=(255,255,255,100))
                for j in i.arrSkin:
                    my_draw.rectangle((i.direction*j[0]*i.size+i.position[2]-25,j[1]*i.size+200,i.direction*j[2]*i.size+i.position[2]-25,j[3]*i.size+200),fill=(251,206,177,100))
        if mario.state=="dead":
            life-=1
            break
        mario_right = 1 if mario.right else -1

        for i in stones:
            mario.stoneHitted(i) #돌에 닿으면 

            i.move(command)
            my_draw.ellipse(tuple(i.position),fill=(255,0,0,100))
        boss.move(command)
        if boss.hp==0:
            isWin = True
            break

        for j in boss.arrBrown:
            my_draw.rectangle((j[0]*boss.size+boss.center[0],j[1]*boss.size+boss.center[1],j[2]*boss.size+boss.center[0],j[3]*boss.size+boss.center[1]),fill=(150,75,0,100))
        for j in boss.arrBlack:
            my_draw.rectangle(j,fill=(0,0,0,25))
            my_draw.rectangle((j[0]*boss.size+boss.center[0],j[1]*boss.size+boss.center[1],j[2]*boss.size+boss.center[0],j[3]*boss.size+boss.center[1]),fill=(0,0,0,100))

        for j in boss.arrWhite:
            my_draw.rectangle(j,fill=(255,255,255,25))
            my_draw.rectangle((j[0]*boss.size+boss.center[0],j[1]*boss.size+boss.center[1],j[2]*boss.size+boss.center[0],j[3]*boss.size+boss.center[1]),fill=(255,255,255,100))
        for j in boss.arrSkin:
            my_draw.rectangle(j,fill=(251,206,177,25))
            my_draw.rectangle((j[0]*boss.size+boss.center[0],j[1]*boss.size+boss.center[1],j[2]*boss.size+boss.center[0],j[3]*boss.size+boss.center[1]),fill=(251,106,177,100))


        height = 0 if mario.state=="normal" else 15 # height는 커진 마리오의 위치를 조정하기 위한 값 
        for i in arrRed:
            my_draw.rectangle((mario_right*i[0]*mario.size+50,i[1]*mario.size+25-height+mario.position[1],mario_right*i[2]*mario.size+50,i[3]*mario.size+25-height+mario.position[1]),fill=(255,0,0,25))
        for i in arrYellow:
            my_draw.rectangle((mario_right*i[0]*mario.size+50,i[1]*mario.size+25-height+mario.position[1],mario_right*i[2]*mario.size+50,i[3]*mario.size+25-height+mario.position[1]),fill=(255,235,203,25))

        for i in arrBrown:
            my_draw.rectangle((mario_right*i[0]*mario.size+50,i[1]*mario.size+25-height+mario.position[1],mario_right*i[2]*mario.size+50,i[3]*mario.size+25-height+mario.position[1]),fill=(165,42,42,25))
        my_draw.text((20,10),"life : "+str(life)+" score : "+str(score),(255,255,255), font=font)


        joystick.disp.image(my_image)

    #while 문을 빠져나왔다는 것은 죽었다는 뜻 
    if isWin:
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0, 0, 0, 100))
        my_draw.text((50,50),"your score : "+str(score),(255,255,255), font=font)
        joystick.disp.image(my_image)
        sleep(3)
        joystick.disp.image(endingImg)
        while(joystick.button_A.value):
            None

        life=3
        main()
    else:
        if life>0:
           
            for i in range(100):
                
                my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(0, 0, 0, i))
        else:
            life=3
        
        joystick.disp.image(my_image)
        main()




        

if __name__ == '__main__':
    main()