import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False


# Кнопки
buttonListValues = [['7', '8', '9'],
                    ['4', '5', '6'],
                    ['1', '2', '3'],
                    ['0', 'K', 'C']]
buttonList = []
for x in range(3):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150

        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))


# Различные переменные
myEquation = ''
delayCounter = 0
testList = []
keyInput = ''
password = '123K4'


# Камера
cap = cv2.VideoCapture(0)
cap.set(3,1280) # размеры фрейма
cap.set(4,720)
detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands = detector.findHands(img, draw=False)

    # Отрисовка интерфейса
    cv2.rectangle(img, (800, 70), (800 + 300, 70 + 100),
                  (225, 225, 225), cv2.FILLED)

    cv2.rectangle(img, (800, 70), (800 + 300, 70 + 100),
                  (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)


    # Обнаружение рук
    if hands:
        # Нахождение расстояние между точками(пальцами)
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]
        # Проверяем что нажал пользователь
        if length < 50 and delayCounter == 0:  # дистанция пальцев для клика!!!
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]  # Проверяем какая кнопка была нажата
                    keyInput += str(myValue)
                    if len(keyInput) >= 6:
                        keyInput = ''
                        myEquation = ''
                    elif keyInput[-1] == 'C':
                        myEquation = ''
                        keyInput = ''    
                    elif keyInput == password:
                        myEquation = 'Open'
                    else:
                        myEquation += myValue
                    delayCounter = 1

                    
    # Избежание многократных кликов
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Выводим финальный текст
    cv2.putText(img, myEquation, (800, 135), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 0, 0), 3, cv2.LINE_AA)

    # Отображение
    key = cv2.waitKey(1)
    cv2.imshow("Image", img)
    if key == ord('c'):
        myEquation = ''