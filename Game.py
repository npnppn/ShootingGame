import pygame
import sys
import random
from time import sleep

r,g,b = 0,0,0
r=random.randrange(0,255)
g=random.randrange(0,255)
b=random.randrange(0,255)
black = (r, g, b)
#기본 바탕화면 색을 랜덤으로 설정.
#원래 현실감있게 검은색만을 주려고 했으나, 배경화면의 색상을 무작위로 표현해야함을 뒤늦게 인지했습니다.. 

pad_width = 800
pad_height = 400
background_width = 900
batImage = ['bat1.png', 'bat2.png', 'bat3.png'] #적군은 3가지 종류

def drawObject(obj,x,y): #객체 그리기
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame(): #게임진행
    global gamepad, aircraft, clock, background1, background2, bullet, explosion

    #비행기 처음 위치
    x = pad_width * 0.05
    y = pad_height * 0.8
    x_change = 0

    #비행기 크기
    aircraftSize = aircraft.get_rect().size
    aircraft_width = aircraftSize[0]
    aircraft_height = aircraftSize[1]
    
    #배경화면 설정
    background1_x = 0
    background2_x = background_width

    #적군 랜덤 생성
    bat = pygame.image.load(random.choice(batImage))
    batSize = bat.get_rect().size #적군크기
    batWidth = batSize[0]
    batHeight = batSize[1]
    
    #적군 초기 위치 설정
    bat_x = random.randrange(0, pad_width/4)
    bat_y = 0
    batSpeed = 1.5

    #총알 좌표 리스트
    bullet_xy = []

    #적군이 총알에 맞을 경우
    isShot = False
    shotCount = 0
    batPassed = 0
    
    crashed = False
    while not crashed: #event 타입이 마우스로 창을 닫는 것이면 crashed의 값을 True로 설정
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #왼쪽 커서버튼 
                    x_change -= 8
                elif event.key == pygame.K_RIGHT: #오른쪽 커서버튼
                    x_change += 8
                elif event.key == pygame.K_SPACE: #스페이스바 버튼
                    bullet_x = x + aircraft_width/2
                    bullet_y = y - aircraft_height
                    bullet_xy.append([bullet_x, bullet_y])              
            if event.type == pygame.KEYUP: #전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        gamepad.fill(black) #마우스로 창을 닫는 이벤트가 아니면 게임판을 랜덤으로 채우고 게임판을 다시 그림
        background1_x -= 2 
        background2_x -= 2

        if background1_x == -background_width: #배경 이미지 복사본을 이용해 배경이 움직이는것처럼 보이게함.
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x,0)
        drawObject(background2, background2_x,0)

        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - aircraft_width:
            x = pad_width - aircraft_width

        if y < bat_y + batHeight: #비행기가 적군과 충돌했는지 체크
            if(bat_x > x and bat_x < x + aircraft_width) or \
                (bat_x + batWidth > x and bat_x + batWidth < x + aircraft_width):
                crash()
        drawObject(aircraft, x, y)

        
        if len(bullet_xy) != 0: #총알 발사 화면에 그리기
            for i, bxy in enumerate(bullet_xy): # 총알 요소에 대해 반복.
                bxy[1] -= 10 #총알의 y좌표 -10 (위로 이동)
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < bat_y: #총알이 적군을 맞추었을 경우
                    if bxy[0] > bat_x and bxy[0] < bat_x + batWidth:
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotCount += 1
                    
                if bxy[1] <= 0: #총알 화면 밖으로 사라짐.
                    try:
                        bullet_xy.remove(bxy) #총알 제거
                    except:
                        pass 

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx,by)

        writeScore(shotCount) #총알 맞춘 점수 표시
        
        bat_x += batSpeed #적군이 왼쪽에서 오른쪽으로 이동

        if bat_x > pad_width: #맨 끝으로 갔을때
            #랜덤으로 새로운 적군 발생
            bat = pygame.image.load(random.choice(batImage))
            batSize = bat.get_rect().size
            batWidth = batSize[0]
            batHeight = batSize[1]
            bat_x = random.randrange(0,pad_width/4)
            bat_y = 0
            batPassed += 1

        writePassed(batPassed) #놓친 적군 표시
        
        if batPassed == 5: #적군 5번 놓치면 게임 오버
            gameOver()

        if isShot: #적군을 맞춘 경우
            #적군 폭발하는 이미지 생성
            drawObject(explosion, bat_x, bat_y) 

            #랜덤으로 새로운 적군 발생
            bat = pygame.image.load(random.choice(batImage))
            batSize = bat.get_rect().size
            batWidth = batSize[0]
            batHeight = batSize[1]
            bat_x = random.randrange(0,pad_width/4)
            bat_y = 0
            isShot = False

            #적군 맞추면 속도 증가
            batSpeed += 0.03
            if batSpeed >= 5:
                batSpeed = 5

        drawObject(bat,bat_x,bat_y) #적군 그리기
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
        
def initGame(): #게임시작
    global gamepad, aircraft, clock, background1, background2, bullet, explosion
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption("ShootingGame made by HyungMin")
    aircraft = pygame.image.load('plane.png')
    background1 = pygame.image.load('background.png')
    background2 = background1.copy() 
    bullet = pygame.image.load('bullet.png')
    explosion = pygame.image.load('explosion.png')
    clock = pygame.time.Clock()

def writeScore(count): #적군을 맞춘 개수 계산
    global gamepad
    font = pygame.font.Font('BMEULJIROTTF.ttf', 40)
    text = font.render('파괴한 적군 수: ' + str(count), True, (255,0,0))
    gamepad.blit(text,(10,0))
    
def writePassed(count): #적군이 화면 통과한 개수
    global gamepad
    font = pygame.font.Font('BMEULJIROTTF.ttf', 40)
    text = font.render('놓친 적군 수: ' + str(count), True, (255,255,0))
    gamepad.blit(text,(350,0))

def showMessage(text): #게임 메시지 출력
    global gamepad
    textfont = pygame.font.Font('BMEULJIROTTF.ttf', 80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

def crash(): #충돌했을 때
    global gamepad
    showMessage('비행기충돌!')

def gameOver(): #게임오버
    global gamepad
    showMessage('게임종료!')

initGame()
runGame()
