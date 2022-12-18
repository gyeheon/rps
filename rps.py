import cv2
import mediapipe as mp
import time
import sys
import math

cap = cv2.VideoCapture(0)


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingers = [True, True, True, True, True]
compare_index = [[6, 8], [10, 12], [14, 16], [18, 20]]

print(hands)

while True:
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
            elif fingers == [True, True, True, True, True]:
                print('ROCK')
            elif fingers == [False, False, False, False, False]:
                print('PAPER')
            elif fingers == [True, True, False, True, True]:
                print('ㅗ')
            else:
                print('IDK')

    cv2.imshow("Image", img)
    cv2.waitKey(1)