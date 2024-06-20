# -*- coding: utf-8 -*-
"""
Created on Sat May  6 14:09:55 2023

@author: PKTAM
"""

import pygame, sys, random
from tkinter import filedialog
from pygame.locals import *
import tkinter as tk
import threading 
from PIL import Image, ImageTk

# Tạo giao diện
root = tk.Tk()
root.title('week 14')
root.geometry('400x300')
# Load ảnh
image = Image.open('img/Menu .png')
photo = ImageTk.PhotoImage(image)

# Hiển thị ảnh trên canvas
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, image=photo, anchor='nw')


def GAME():
    ####################################
    #PHẦN 1: ĐỊNH NGHĨA CÁC THAM SỐ ##
    #####################################
    ###KÍCH THƯỚC KHUNG MÀN HÌNH GAME
    WINDOWWIDTH = 400
    WINDOWHEIGHT = 600
    ###KHỞI TẠO THƯ VIỆN ĐỂ DÙNG
    pygame.init()
    ##TỐC ĐỘ KHUNG HÌNH CỦA VIDEO
    FPS = 60 # Famres Per Second
    fpsClock = pygame.time.Clock() #Lặp theo nhịp clock (tham số FPS) 
    ####################################
    #####PHẦN 2: NỀN GAME ##############
    #####################################
    #TỐC ĐỘ CUỘN NỀN
    BGSPEED = 10 # tốc độ cuộn nền
    # Hình nền
    BGIMG_1 = pygame.image.load('img/background01.png')
    BGIMG_2 = pygame.image.load('img/background02.png')
    # LAYER (SURFACE) NỀN
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('45 Bùi Thiên Kim = Ex7.5: Game = Game ĐUA XE')
    # LỚP HÌNH NỀN = CUỘN NỀN
    class Background():
        def __init__(self, img, speed):
            self.x = 0
            self.y = 0
            self.speed = speed
            self.img = img
            self.width = self.img.get_width()
            self.height = self.img.get_height()

        def draw(self):
            DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
            DISPLAYSURF.blit(self.img, (int(self.x), int(self.y-self.height)))
            
        def update(self):
            self.y += self.speed
            if self.y > self.height:
                self.y -= self.height

        def handle_event(self):
            if self.img is BGIMG_1:
                self.img = BGIMG_2
            elif self.img is BGIMG_2:
                self.img = BGIMG_1
            return self.img
            
        def bgSpeed(self):
            if self.speed < 200:
                self.speed += 10
            else:
                self.speed = 10
            return self.speed
            
    class FPSSpeed():
        def __init__(self, speed):
            self.speed = speed
                
        def fpsSpeed(self):
            if self.speed < 200:
                self.speed += 10
            else:
                self.speed = 60
            return self.speed
    ####################################
    #####PHẦN 3: XE TRONG GAME #########
    """
    • X_MARGIN là lề hai bên trái và phải (xe không được vượt qua đó).
    • CARWIDTH và CARHEIGHT là kích thước của xe.
    • CARSPEED là tốc độ di chuyển (tiến, lùi, trái, phải) của xe.
    • CARIMG là ảnh chiếc xe.
    """
    #####################################
    #KÍCH THƯỚC XE
    X_MARGIN = 80
    CARWIDTH = 40
    CARHEIGHT = 60
    CARSPEED = 3
    CARIMG_1 = pygame.image.load('img/car.png')
    CARIMG_2 = pygame.image.load('img/car1.png')
    CARIMG_3 = pygame.image.load('img/car2.png')
    CARIMG_4 = pygame.image.load('img/car3.png')
    CARIMG_5 = pygame.image.load('img/car4.png')
    #LỚP XE TRONG GAME
    class Car():
        def __init__(self, img):
            self.width = CARWIDTH
            self.height = CARHEIGHT
            self.x = (WINDOWWIDTH-self.width)/2
            self.y = (WINDOWHEIGHT-self.height)/2
            self.img = img
            self.speed = CARSPEED
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill((255, 255, 255))
        def draw(self):
            DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        def appear(self):
            self.x = WINDOWWIDTH - (WINDOWWIDTH-self.width)/3 - self.width
            DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        def update(self, moveLeft, moveRight, moveUp, moveDown):
            if moveLeft == True:
                self.x -= self.speed
            if moveRight == True:
                self.x += self.speed
            if moveUp == True:
                self.y -= self.speed
            if moveDown == True:
                self.y += self.speed

            if self.x < X_MARGIN:
                self.x = X_MARGIN
            if self.x + self.width > WINDOWWIDTH - X_MARGIN:
                self.x = WINDOWWIDTH - X_MARGIN - self.width
            if self.y < 0:
                self.y = 0
            if self.y + self.height > WINDOWHEIGHT :
                self.y = WINDOWHEIGHT - self.height
        def handle_event(self):
            if self.img is CARIMG_1:
                self.img = CARIMG_2
            elif self.img is CARIMG_2:
                self.img = CARIMG_3
            elif self.img is CARIMG_3:
                self.img = CARIMG_4
            elif self.img is CARIMG_4:
                self.img = CARIMG_5
            elif self.img is CARIMG_5:
                self.img = CARIMG_1
            return self.img
    ####################################
    #PHẦN 4: XE CHƯỚNG NGẠI VẬT = XE NGƯỢC CHIỀU:obstacles ##
    """
    • LANEWIDTH là độ rộng của 1 làn xe (đường có 4 làn).
    • DISTANCE là khoảng cách giữa các xe theo chiều dọc.
    • OBSTACLESSPEED là tốc độ ban đầu của những chiếc xe.
    • CHANGESPEED dùng để tăng tốc độ của những chiếc xe theo thời gian.
    • OBSTACLESIMG là ảnh chiếc xe.
    """
    #####################################
    LANEWIDTH = 60
    DISTANCE = 200
    OBSTACLESSPEED = 2
    CHANGESPEED = 0.001
    OBSTACLESIMG_1 = pygame.image.load('img/xe.png')
    OBSTACLESIMG_2 = pygame.image.load('img/xe1.png')
    OBSTACLESIMG_3 = pygame.image.load('img/xe2.png')
    OBSTACLESIMG_4 = pygame.image.load('img/xe3.png')
    OBSTACLESIMG_5 = pygame.image.load('img/xe4.png')
    class Obstacles():
        def __init__(self, img):
            self.width = CARWIDTH
            self.height = CARHEIGHT
            self.x = (WINDOWWIDTH-self.width)/3
            self.y = (WINDOWHEIGHT-self.height)/2
            self.img = img
            self.distance = DISTANCE
            self.speed = OBSTACLESSPEED
            self.changeSpeed = CHANGESPEED
            self.ls = []
            for i in range(5):
                y = -CARHEIGHT-i*self.distance
                lane = random.randint(0, 3)
                self.ls.append([lane, y])
        def draw(self):
            for i in range(5):
                self.x = int(X_MARGIN + self.ls[i][0]*LANEWIDTH + (LANEWIDTH-self.width)/2)
                self.y = int(self.ls[i][1])
                DISPLAYSURF.blit(self.img, (self.x, self.y))
        def appear(self):
            DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        def update(self):
            for i in range(5):
                self.ls[i][1] += self.speed
            self.speed += self.changeSpeed
            if self.ls[0][1] > WINDOWHEIGHT:
                self.ls.pop(0)
                y = self.ls[3][1] - self.distance
                lane = random.randint(0, 3)
                self.ls.append([lane, y])
        def handle_event(self):
            if self.img is OBSTACLESIMG_1:
                self.img = OBSTACLESIMG_2
            elif self.img is OBSTACLESIMG_2:
                self.img = OBSTACLESIMG_3
            elif self.img is OBSTACLESIMG_3:
                self.img = OBSTACLESIMG_4
            elif self.img is OBSTACLESIMG_4:
                self.img = OBSTACLESIMG_5
            elif self.img is OBSTACLESIMG_5:
                self.img = OBSTACLESIMG_1
            return self.img
    ####################################
    #PHẦN 5: TÍNH ĐIỂM ##
    #####################################
    class Score():
        def __init__(self):
            self.score = 0
        def draw(self):
            font = pygame.font.SysFont('consolas', 30)
            scoreSuface = font.render('Score: '+str(int(self.score)), True, (0, 0, 0))
            DISPLAYSURF.blit(scoreSuface, (10, 10))
        def update(self):
            self.score += 0.02
    ####################################
    #PHẦN 6: XỬ LÝ VA CHẠM: Collision ##
    #####################################
    def rectCollision(rect1, rect2):
        if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
            return True
        return False
    def isGameover(car, obstacles):
        carRect = [car.x, car.y, car.width, car.height]
        for i in range(5):
            x = int(X_MARGIN + obstacles.ls[i][0]*LANEWIDTH + (LANEWIDTH-obstacles.width)/2)
            y = int(obstacles.ls[i][1])
            obstaclesRect = [x, y, obstacles.width, obstacles.height]
            if rectCollision(carRect, obstaclesRect) == True:
                return True
        return False
    ####################################
    #PHẦN 7: CÁC THỦ TỤC CHƠI GAME ##
    """
    • gameStart() là phần chuẩn bị khi vừa mở game lên.
    • gamePlay() là phần chơi chính.
    • gameOver() là phần xuất hiện khi thua 1 màn chơi.
    """
    #####################################
    def gameOver(bg, car, obstacles, score, fps):
        font = pygame.font.SysFont('consolas', 60)
        headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
        headingSize = headingSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 25)
        commentSuface = font.render('Press "space" to replay', True, (255, 0, 0))
        commentSize = commentSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        backgroundOption = font.render('Press "b" to change background', True, (0, 0, 0))
        backgroundSize = backgroundOption.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        option = font.render('Option', True, (0, 0, 255))
        optionSize = option.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        carOption = font.render('Press "c" to change player color', True, (0, 0, 0))
        carSize = carOption.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        obstaclesOption = font.render('Press "o" to change obstacles color', True, (0, 0, 0))
        obstaclesSize = obstaclesOption.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        bgSpeedOption = font.render('Press "g" to change background speed', True, (0, 0, 0))
        bgSpeedOptionSize = bgSpeedOption.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        bgSpeed = font.render(str(bg.speed), True, (255, 0, 0))
        bgSpeedSize = bgSpeed.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        fpsSpeedOption = font.render('Press "f" to change FPS', True, (0, 0, 0))
        fpsSpeedOptionSize = fpsSpeedOption.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        fpsSpeed = font.render(str(fps.speed), True, (255, 0, 0))
        fpsSpeedSize = fpsSpeed.get_size()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_SPACE:
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == K_b:
                        bg.handle_event()
                    if event.key == K_c:
                        car.handle_event()
                    if event.key == K_o:
                        obstacles.handle_event()
                    if event.key == K_g:
                        bg.bgSpeed() 
                        font = pygame.font.SysFont('consolas', 20)
                        bgSpeed = font.render(str(bg.speed), True, (255, 0, 0))
                        bgSpeedSize = bgSpeed.get_size()
                    if event.key == K_f:
                        fps.fpsSpeed()
                        font = pygame.font.SysFont('consolas', 20)
                        fpsSpeed = font.render(str(fps.speed), True, (255, 0, 0))
                        fpsSpeedSize = fpsSpeed.get_size()
                        
            bg.draw()
            car.draw()
            obstacles.draw()
            score.draw()
            DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
            DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 350))
            DISPLAYSURF.blit(option, (int((WINDOWWIDTH - optionSize[0])/2), 390))
            DISPLAYSURF.blit(backgroundOption, (int((WINDOWWIDTH - backgroundSize[0])/2), 420))
            DISPLAYSURF.blit(carOption, (int((WINDOWWIDTH - carSize[0])/2), 450))
            DISPLAYSURF.blit(obstaclesOption, (int((WINDOWWIDTH - obstaclesSize[0])/2), 480))
            DISPLAYSURF.blit(bgSpeedOption, (int((WINDOWWIDTH - bgSpeedOptionSize[0])/2), 510))
            DISPLAYSURF.blit(bgSpeed, (int((WINDOWWIDTH - bgSpeedSize[0])/2), 530))
            DISPLAYSURF.blit(fpsSpeedOption, (int((WINDOWWIDTH - fpsSpeedOptionSize[0])/2), 550))
            DISPLAYSURF.blit(fpsSpeed, (int((WINDOWWIDTH - fpsSpeedSize[0])/2), 570))
            pygame.display.update()
            fpsClock.tick(fps.speed)
            
    def gameStart(bg, car, obstacles, fps):
        bg.__init__(bg.img, bg.speed)
        car.__init__(car.img)
        obstacles.__init__(obstacles.img)
        fps.__init__(fps.speed)
        font = pygame.font.SysFont('consolas', 60)
        headingSuface = font.render('RACING', True, (255, 0, 0))
        headingSize = headingSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        playerSuface = font.render('Player', True, (0, 0, 255))
        playerSize = playerSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        obstaclesSuface = font.render('Obstacles', True, (0, 0, 255))
        obstaclesSize = obstaclesSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        option = font.render('Option', True, (0, 0, 255))
        optionSize = option.get_size()

        font = pygame.font.SysFont('consolas', 25)
        commentSuface = font.render('Press "space" to play', True, (255, 0, 0))
        commentSize = commentSuface.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        backgroundOption = font.render('Press "b" to change background', True, (0, 0, 0))
        backgroundSize = backgroundOption.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        carOption = font.render('Press "c" to change car color', True, (0, 0, 0))
        carSize = carOption.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        obstaclesOption = font.render('Press "o" to change obstacles color', True, (0, 0, 0))
        obstaclesOptSize = obstaclesOption.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        bgSpeedOption = font.render('Press "g" to change background speed', True, (0, 0, 0))
        bgSpeedOptionSize = bgSpeedOption.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        bgSpeed = font.render(str(bg.speed), True, (255, 0, 0))
        bgSpeedSize = bgSpeed.get_size()
        
        font = pygame.font.SysFont('consolas', 15)
        fpsSpeedOption = font.render('Press "f" to change FPS', True, (0, 0, 0))
        fpsSpeedOptionSize = fpsSpeedOption.get_size()
        
        font = pygame.font.SysFont('consolas', 20)
        fpsSpeed = font.render(str(fps.speed), True, (255, 0, 0))
        fpsSpeedSize = fpsSpeed.get_size()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_SPACE:
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == K_b:
                        bg.handle_event()
                    if event.key == K_c:
                        car.handle_event()
                    if event.key == K_o:
                        obstacles.handle_event()
                    if event.key == K_g:
                        bg.bgSpeed()  
                        font = pygame.font.SysFont('consolas', 20)
                        bgSpeed = font.render(str(bg.speed), True, (255, 0, 0))
                        bgSpeedSize = bgSpeed.get_size()
                    if event.key == K_f:
                        fps.fpsSpeed()
                        font = pygame.font.SysFont('consolas', 20)
                        fpsSpeed = font.render(str(fps.speed), True, (255, 0, 0))
                        fpsSpeedSize = fpsSpeed.get_size()
            bg.draw()
            car.appear()
            obstacles.appear()
            DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
            DISPLAYSURF.blit(playerSuface, (int(WINDOWWIDTH - (WINDOWWIDTH - playerSize[0])/3 - playerSize[0] + 5), int((WINDOWHEIGHT - playerSize[0])/2) - 20))
            DISPLAYSURF.blit(obstaclesSuface, (int((WINDOWWIDTH - obstaclesSize[0])/3 - 5), int((WINDOWHEIGHT - obstaclesSize[0])/2- 5)))
            DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 350))
            DISPLAYSURF.blit(option, (int((WINDOWWIDTH - optionSize[0])/2), 390))
            DISPLAYSURF.blit(backgroundOption, (int((WINDOWWIDTH - backgroundSize[0])/2), 420))
            DISPLAYSURF.blit(carOption, (int((WINDOWWIDTH - carSize[0])/2), 450))
            DISPLAYSURF.blit(obstaclesOption, (int((WINDOWWIDTH - obstaclesOptSize[0])/2), 480))
            DISPLAYSURF.blit(bgSpeedOption, (int((WINDOWWIDTH - bgSpeedOptionSize[0])/2), 510))
            DISPLAYSURF.blit(bgSpeed, (int((WINDOWWIDTH - bgSpeedSize[0])/2), 530))
            DISPLAYSURF.blit(fpsSpeedOption, (int((WINDOWWIDTH - fpsSpeedOptionSize[0])/2), 550))
            DISPLAYSURF.blit(fpsSpeed, (int((WINDOWWIDTH - fpsSpeedSize[0])/2), 570))
            pygame.display.update()
            fpsClock.tick(fps.speed)          
            
    def gamePlay(bg, car, obstacles, score, fps):
        car.__init__(car.img)
        obstacles.__init__(obstacles.img)
        bg.__init__(bg.img, bg.speed)
        fps.__init__(fps.speed)
        score.__init__()
        moveLeft = False
        moveRight = False
        moveUp = False
        moveDown = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        moveLeft = True
                    if event.key == K_RIGHT:
                        moveRight = True
                    if event.key == K_UP:
                        moveUp = True
                    if event.key == K_DOWN:
                        moveDown = True
                        
                    if event.key == K_a:
                        moveLeft = True
                    if event.key == K_d:
                        moveRight = True
                    if event.key == K_w:
                        moveUp = True
                    if event.key == K_s:
                        moveDown = True
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        moveLeft = False
                    if event.key == K_RIGHT:
                        moveRight = False
                    if event.key == K_UP:
                        moveUp = False
                    if event.key == K_DOWN:
                        moveDown = False
                        
                    if event.key == K_a:
                        moveLeft = False
                    if event.key == K_d:
                        moveRight = False
                    if event.key == K_w:
                        moveUp = False
                    if event.key == K_s:
                        moveDown = False
                        
            if isGameover(car, obstacles):
                return
            bg.draw()
            bg.update()
            car.draw()
            car.update(moveLeft, moveRight, moveUp, moveDown)
            obstacles.draw()
            obstacles.update()
            score.draw()
            score.update()
            pygame.display.update()
            fpsClock.tick(fps.speed)
    ####################################
    #PHẦN 8: HÀM MAIN ##
    #####################################
    def main():
        fps = FPSSpeed(FPS)
        bg = Background(BGIMG_1, BGSPEED)
        car = Car(CARIMG_1)
        obstacles = Obstacles(OBSTACLESIMG_1)
        score = Score()
        gameStart(bg, car, obstacles, fps)
        while True:
            gamePlay(bg, car, obstacles, score, fps)
            gameOver(bg, car, obstacles, score, fps)
    if __name__ == '__main__':
        main()
def startGame():
    game_thread = threading.Thread(target=GAME)
    game_thread.start()
    
def Quit():
    root.destroy()
    

# Tạo nút goi GAME
game_button = tk.Button(canvas, text='START', command=startGame)
game_button.place(x=170, y=50)

exit_button = tk.Button(canvas, text='Exit', command=Quit)
exit_button.place(x=176, y=180)


# Chạy chương trình
root.mainloop()
