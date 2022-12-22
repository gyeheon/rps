import cv2
import mediapipe as mp
import time
import sys
import math
import keyboard
import pygame

cap = cv2.VideoCapture(0)





pygame.init()

size = width, height = 1920, 1080
ImageList = ['five','four','three','two','one','rock','scissor','paper','error','start']
Images = []
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
clock = pygame.time.Clock()
color = (0, 0, 0)
level = 0

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))

mpHands = mp.solutions.hands
hands = mpHands.Hands() 
mpDraw = mp.solutions.drawing_utils
fingers = [True, True, True, True, True]
compare_index = [[6, 8], [10, 12], [14, 16], [18, 20]]
print(hands)

for i in ImageList:
    Images.append(pygame.image.load(f"image/{i}.png"))



def hand_cheaker():
    rps = 7

    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


            def landmark_index(a):
                return dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[a].x, handLms.landmark[a].y)


            for i in range(1, 5):
                if landmark_index(compare_index[i - 1][1]) < landmark_index(compare_index[i - 1][0]):
                    fingers[i] = True
                else:
                    fingers[i] = False
            if abs(dist(handLms.landmark[4].x, handLms.landmark[4].y, handLms.landmark[17].x,
                        handLms.landmark[17].y)) < landmark_index(17):
                fingers[0] = True
            else:
                fingers[0] = False

            if fingers == [False, False, True, True, True] or fingers == [True, False, False, True, True]:
                print('SCISSORS')
                rps = 1
            elif fingers == [True, True, True, True, True]:
                print('ROCK')
                rps = 0
            elif fingers == [False, False, False, False, False]:
                print('PAPER')
                rps = 2
            elif fingers == [True, True, False, True, True]:
                print('ㅗ')
            else:
                print('IDK')
                rps = 4
    return rps

    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

while True:
    clock.tick(30)
    screen.fill(color)

    if level == 0:
        screen.blit(Images[9], (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level = 1
    

    
    #level1
    if level == 1:
        for i in Images[:5]:
            screen.fill((0,0,0))
            screen.blit(i, (610,190))
            time.sleep(1)
            pygame.display.update()
        
        human = hand_cheaker()
        print(human)
        if human == 0:
            screen.fill((0,0,0))
            screen.blit(Images[7], (460,40))
        elif human == 1:
            screen.fill((0,0,0))
            screen.blit(Images[5], (460,40))
        elif human == 2:
            screen.fill((0,0,0))
            screen.blit(Images[6], (460,40))
        elif human == (4 or 7):
            screen.fill((0,0,0))
            screen.blit(Images[8], (460,40))
        
        time.sleep(1)
        pygame.display.update()

        time.sleep(5)
        level = 0   

    pygame.display.update()
 