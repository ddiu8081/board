# !C:/Users/Administrator/Desktop/demo/python
# coding=utf-8

# 导入pygame库
import os

import pygame, random, sys, time  # sys模块中的exit用于退出
from pygame.locals import *
import pickle


# 定义一个飞机基类
class Plane(object):
    def __init__(self):
        self.bulletList = []

    # 描绘飞机
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# 玩家飞机类，继承基类
class Hero(Plane):

    def __init__(self):
        Plane.__init__(self)
        planeImageName = 'Resources/hero.png'
        self.image = pygame.image.load(planeImageName).convert()
        # 玩家原始位置
        self.x = 200
        self.y = 600
        self.planeName = 'hero'

    # 键盘控制自己飞机
    def keyHandle(self, keyValue):
        if keyValue == 'left':
            self.x -= 1
        elif keyValue == 'right':
            self.x += 1


# 定义敌人飞机类
class Enemy(Plane):
    """docstring for Enemy"""

    def __init__(self, speed):
        super(Enemy, self).__init__()
        randomImageNum = random.randint(1, 4)
        planeImageName = 'Resources/fruit/' + str(randomImageNum) + '.png'
        self.image = pygame.image.load(planeImageName).convert_alpha()
        # 敌人飞机原始位置
        self.x = random.randint(20, 400)  # 敌机出现的位置任意
        self.y = 0
        self.planeName = 'enemy'
        self.direction = 'down'  # 用英文表示
        self.speed = speed  # 移动速度,这个参数现在需要传入

    def move(self):
        if self.direction == 'down':
            self.y += self.speed  # 飞机不断往下掉


# 定义炸弹
class Enemybullet(Plane):
    """docstring for Enemy"""

    def __init__(self, speed):
        super(Enemybullet, self).__init__()
        planeImageName = 'Resources/bomb.png'
        self.image = pygame.image.load(planeImageName).convert_alpha()
        # 炸弹原始位置
        self.x = random.randint(20, 400)  # 炸弹出现的位置任意
        self.y = 0
        self.planeName = 'enemy'
        self.direction = 'down'  # 用英文表示
        self.speed = speed  # 移动速度,这个参数现在需要传入

    def move(self):
        if self.direction == 'down':
            self.y += self.speed  # 飞机不断往下掉


class GameInit(object):
    """GameInit"""
    # 类属性
    gameLevel = 1  # 简单模式
    g_fruitList = []  # 前面加上g类似全局变量
    g_bombList = []  # 前面加上g类似全局变量
    score = 0  # 用于统计分数
    life = 3  # 用来统计生命
    hero = object

    @classmethod
    def createEnemy(cls, speed):
        cls.g_fruitList.append(Enemy(speed))

    @classmethod
    def createEnemybullet(cls, speed):
        cls.g_bombList.append(Enemybullet(speed))

    @classmethod
    def createHero(cls):
        cls.hero = Hero()

    @classmethod
    def gameInit(cls):
        cls.createHero()

    @classmethod
    def heroPlaneKey(cls, keyValue):
        cls.hero.keyHandle(keyValue)

    @classmethod
    def draw(cls, screen):
        delPlaneList = []
        delPlanebulletList = []
        j = 0
        s = 0
        heroRect = pygame.Rect(cls.hero.image.get_rect())
        heroRect.left = cls.hero.x
        heroRect.top = cls.hero.y
        for i in cls.g_fruitList:
            i.draw(screen)  # 画出敌机
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top = i.y
            # 敌机超过屏幕或者撞到就从列表中删除
            if heroRect.colliderect(enemyRect):
                # if enemyRect.width == 39:
                #     cls.score += 100  # 小中大飞机分别100,500,1000分
                # if enemyRect.width == 60:
                #     cls.score += 500
                # if enemyRect.width == 78:
                #     cls.score += 1000
                cls.score += 100

                delPlaneList.append(j)
                j += 1
            if i.y > 680:
                delPlaneList.append(j)
                j += 1

        for m in delPlaneList:
            del cls.g_fruitList[m]

        for i in cls.g_bombList:
            i.draw(screen)  # 画出炸弹
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top = i.y
            # 炸弹超过屏幕或者撞到就从列表中删除
            if i.y > 680:
                delPlanebulletList.append(s)
                s += 1

            if heroRect.colliderect(enemyRect):
                time.sleep(0.3)

                cls.life -= 1
                delPlanebulletList.append(s)
                s += 1
                print(cls.life)

        for m in delPlanebulletList:
            del cls.g_bombList[m]

        delBulletList = []
        j = 0
        s = 0
        cls.hero.draw(screen)  # 画出英雄飞机位置

    @classmethod
    def setXY(cls):
        for i in cls.g_fruitList:
            i.move()
        for i in cls.g_bombList:
            i.move()

            # 判断游戏是否结束

    @classmethod
    def gameover(cls):
        if cls.life == 0:
            return True

    # 游戏结束后等待玩家按键
    @classmethod
    def waitForKeyPress(cls):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:  # Enter按键
                        return

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit(0)

    @staticmethod
    def pause(surface, image):
        surface.blit(image, (0, 0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        return

    @staticmethod
    def drawText(text, font, surface, x, y):
        # 参数1：显示的内容 |参数2：是否开抗锯齿，True平滑一点|参数3：字体颜色|参数4：字体背景颜色
        content = font.render(text, False, (10, 100, 200))
        contentRect = content.get_rect()
        contentRect.left = x
        contentRect.top = y
        surface.blit(content, contentRect)


def main():
    # 初始化pygame
    pygame.init()
    # 创建一个窗口与背景图片一样大
    ScreenWidth, ScreenHeight = 460, 680
    easyEnemySleepTime = 1  # 简单模式下每隔1s创建新的敌机
    middleEnemySleepTime = 0.5
    hardEnemySleepTime = 0.25
    lastEnemyTime = 0
    pos = ''
    screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), 0, 32)
    pygame.display.set_caption('圣诞老人接水果')
    # 参数1：字体类型，例如"arial"  参数2：字体大小
    font = pygame.font.SysFont(None, 64)
    font1 = pygame.font.SysFont("arial", 24)
    font2 = pygame.font.SysFont("arial", 30)
    # 记录游戏开始的时间
    startTime = time.time()
    # 背景图片加载并转换成图像
    background = pygame.image.load("Resources/bg_01.png").convert()  # 背景图片
    gameover = pygame.image.load("Resources/gameover.png").convert()  # 游戏结束图片
    start = pygame.image.load("Resources/startone.png")  # 游戏开始图片
    gamePauseIcon = pygame.image.load("Resources/Pause.png")
    gameStartIcon = pygame.image.load("Resources/Start.png")
    screen.blit(start, (0, 0))
    pygame.display.update()  # 开始显示启动图片，直到有Enter键按下才会开始
    GameInit.waitForKeyPress()
    # 初始化
    GameInit.gameInit()
    while True:
        if os.path.exists('score.txt'):
            f = open('score.txt', 'r')
            historyscore = f.readline()
        else:
            f = open('score.txt', 'w+')
            f.write('0')
            historyscore = 0
        # try:
        #     f = open('score.txt','r')
        # except FileNotFoundError:
        #     f = open('score.txt', 'w+')
        #     f.write('0')
            # historyscore = 0
        # historyscore = f.readline()
        screen.blit(background, (0, 0))  # 不断覆盖，否则在背景上的图片会重叠
        screen.blit(gameStartIcon, (350, 0))  # 把这个图片换成爱代表生命的爱心
        screen.blit(gamePauseIcon, (0, 0))
        GameInit.drawText('%s' % (GameInit.life), font2, screen, 400, 10)
        GameInit.drawText('score:%s' % (GameInit.score), font1, screen, 80, 15)
        if int(GameInit.score) < int(historyscore):
            GameInit.drawText('best:%s' % (historyscore), font1, screen, 80, 35)
        else:
            GameInit.drawText('best:%s' % (GameInit.score), font1, screen, 80, 35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameInit.terminate()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT:
                    pos = 'right'
                if event.key == K_LEFT:
                    pos = 'left'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            elif event.type == KEYUP:
                pos = ''

        if (pos == 'right'):
            GameInit.heroPlaneKey('right')
        elif (pos == 'left'):
            GameInit.heroPlaneKey('left')

        interval = time.time() - startTime
        # easy模式
        if interval < 10:
            if time.time() - lastEnemyTime >= easyEnemySleepTime:
                GameInit.createEnemy(0.8)  # 传入的参数是speed
                GameInit.createEnemybullet(0.5)
                lastEnemyTime = time.time()
        # middle模式
        elif interval >= 10 and interval < 30:
            if time.time() - lastEnemyTime >= middleEnemySleepTime:
                GameInit.createEnemy(1)
                GameInit.createEnemybullet(0.5)
                lastEnemyTime = time.time()
        # hard模式
        elif interval >= 30:
            if time.time() - lastEnemyTime >= hardEnemySleepTime:
                GameInit.createEnemy(1.2)
                GameInit.createEnemybullet(0.5)
                lastEnemyTime = time.time()
        GameInit.setXY()
        GameInit.draw(screen)  # 描绘类的位置
        pygame.display.update()  # 不断更新图片
        if GameInit.gameover():
            time.sleep(1)  # 睡1s时间,让玩家看到与敌机相撞的画面
            screen.blit(gameover, (0, 0))
            GameInit.drawText('%s' % (GameInit.score), font, screen, 170, 400)
            f = open('score.txt','r')
            historyscore = f.readline()
            if int(GameInit.score) > int(historyscore):
                f = open('score.txt', 'w')
                f.write(str(GameInit.score))
                f.close()
            pygame.display.update()
            GameInit.waitForKeyPress()
            break


if __name__ == '__main__':
    main()
