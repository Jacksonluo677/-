import math
import pygame
import random

#初始化界面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('源源打飞机')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.png')
playerImg = pygame.image.load('player.png')

#飞机初始位置
PlayerX = 360
PlayerY = 480
PlayerStepX = 0 #X的速度
PlayerStepY = 0 #Y的速度

#分数
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
def show_score():
    text = f"SCORE {score}"
    score_render = font.render(text,True,(255,255,255))
    screen.blit(score_render,(10,10))

#结束游戏
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64)
def check_is_over():
    global is_over
    if is_over:
        text = "!GAME OVER!"
        score_render = over_font.render(text, True, (255, 0, 0))
        screen.blit(score_render, (164, 164))

#添加音乐
#BGM
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1)

#音效
hit_sound = pygame.mixer.Sound('exp.wav')
shoot_sound = pygame.mixer.Sound('laser.wav')

#敌人类
number_of_enemies = 6
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('enemy.png')
        self.x = random.randint(100, 700)
        self.y = random.randint(50,200)
        self.step = random.randint(2,4)
    #重生
    def reset(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(50, 200)

#保存敌人
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())

def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.img,(e.x,e.y))
        e.x += e.step
        e.y += 0.2
        if e.x >736 or e.x < 0:
            e.step *= -1
            if e.y > 350:
                is_over = True
                enemies.clear()
#子弹类
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = PlayerX + 16
        self.y = PlayerY - 10
        self.step = 10
    #击中
    def hit(self):
        global score
        for e in enemies:
            if distance(self.x,self.y,e.x,e.y) < 40:
                #射中
                hit_sound.play()
                bullet.remove(self)
                e.reset()
                score += 10

bullet = []#保存子弹
def show_bullet():
    for b in bullet:
        screen.blit(b.img,(b.x,b.y))
        b.hit()
        b.y -= b.step
        if b.y < 0:
            bullet.remove(b)

#欧氏距离
def distance(bx,by,ex,ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a*a + b*b)

#事件输入
def process_event():
    global PlayerStepX
    global PlayerStepY
    # 键盘
    if event.type == pygame.KEYDOWN:  # 按下移动
        if event.key == pygame.K_RIGHT:
            PlayerStepX = 5
        if event.key == pygame.K_LEFT:
            PlayerStepX = -5
        if event.key == pygame.K_DOWN:
            PlayerStepY = 5
        if event.key == pygame.K_UP:
            PlayerStepY = -5
        if event.key == pygame.K_SPACE:
            bullet.append(Bullet())
            shoot_sound

    if event.type == pygame.KEYUP:  # 松开不动
        PlayerStepX = 0
        PlayerStepY = 0

#飞机移动
def player_move():
    global PlayerX
    global PlayerY
    PlayerX += PlayerStepX
    PlayerY += PlayerStepY
    # 防范出界
    if PlayerX > 736:
        PlayerX = 736
    if PlayerX < 0:
        PlayerX = 0
    if PlayerY < 0:
        PlayerY = 0
    if PlayerY > 536:
        PlayerY = 536

#主函数

running = True
while True:
    screen.blit(bgImg,(0,0))
    show_score()
    for event in pygame.event.get():#输入事件
        process_event()#处理事件
        if event.type == pygame.QUIT:
            running = False

    screen.blit(playerImg, (PlayerX, PlayerY))
    player_move()
    show_enemy()
    show_bullet()
    check_is_over()
    pygame.display.update()#让其一直更新上传，保持一个动画形态