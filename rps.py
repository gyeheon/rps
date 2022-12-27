import cv2
import mediapipe as mp
import time
import math
import keyboard
import pygame
import random

pygame.init()
cap = cv2.VideoCapture(0)
size = width, height = 1920, 1080
ImageList = ['five','four','three','two','one','rock','scissor','paper','error','start','computerwin','draw','humanwin']
Images = {}
for i in ImageList:
    Images[i] = (pygame.image.load(f"image/{i}.jpg"))
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
clock = pygame.time.Clock()
color = (0, 0, 0)
level = 0
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingers = [True, True, True, True, True]
compare_index = [[6, 8], [10, 12], [14, 16], [18, 20]]

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))

def hand_cheaker():
    rps = "nohand"
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
                rps = "scissor"
            elif fingers == [True, True, True, True, True]:
                rps = "rock"
            elif fingers == [False, False, False, False, False]:
                rps = "paper"
            else:
                rps = "other"
    return rps

def show_image(computer_hand, whowin):
    screen.fill((0,0,0))
    screen.blit(Images[computer_hand], (0,0))
    screen.blit(Images[whowin], (0,0))
        
def pro_cheak():
    pro = random.randint(1,100)
    if pro < 31:
        pro_result = "draw"
    elif pro > 40:
        pro_result = "computerwin"
    else:
        pro_result = "humanwin"
    return pro_result

while True:
    clock.tick(30)
    screen.fill(color)
    if level == 0:
        screen.blit(Images["start"], (0,0))
        pygame.display.update()
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level = 1

    if level == 1:
        for i in list(Images.values())[:5]:
            screen.fill((0,0,0))
            screen.blit(i, (0,0))
            time.sleep(1)
            pygame.display.update()
        time.sleep(1)

        whowin = pro_cheak()
        human = hand_cheaker()
        print("human", human)
        if human == "rock":
            if whowin == "draw":
                show_image("rock", whowin)
            elif whowin == "computerwin":
                show_image("paper", whowin)
            elif whowin == "humanwin":
                show_image("scissor", whowin)
        elif human == "scissor":
            if whowin == "draw":
                show_image("scissor", whowin)
            elif whowin == "computerwin":
                show_image("rock", whowin)
            elif whowin == "humanwin":
                show_image("paper", whowin)
        elif human == "paper":
            if whowin == "draw":
                show_image("paper", whowin)
            elif whowin == "computerwin":
                show_image("scissor", whowin)
            elif whowin == "humanwin":
                show_image("rock", whowin)
        elif human in ['other','nohand']:
            screen.fill((0,0,0))
            screen.blit(Images["error"], (0,0))
        pygame.display.update()
        time.sleep(5)
        level = 0
    pygame.display.update()
 
