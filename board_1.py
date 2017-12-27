#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
# 定义颜色变量
greyColour = pygame.Color(150,150,150)

class GameInit(object):
    """GameInit"""
    # 类属性
    gameLevel = 1  # 简单模式
    g_ememyList = []  # 前面加上g类似全局变量
    score = 0  # 用于统计分数
    hero = object

    @classmethod
    def createEnemy(cls, speed):
        cls.g_ememyList.append(Enemy(speed))

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
        j = 0
        for i in cls.g_ememyList:
            i.draw(screen)  # 画出敌机
            # 敌机超过屏幕就从列表中删除
            if i.y > 680:
                delPlaneList.append(j)
            j += 1
        for m in delPlaneList:
            del cls.g_ememyList[m]

        delBulletList = []
        j = 0
        cls.hero.draw(screen)  # 画出英雄飞机位置
        for i in cls.hero.bulletList:
            # 描绘英雄飞机的子弹，超出window从列表中删除
            i.draw(screen)
            if i.y < 0:
                delBulletList.append(j)
            j += 1
        # 删除加入到delBulletList中的导弹索引,是同步的
        for m in delBulletList:
            del cls.hero.bulletList[m]

            # 更新敌人飞机位置

    @classmethod
    def setXY(cls):
        for i in cls.g_ememyList:
            i.move()

    # 自己飞机发射子弹
    @classmethod
    def shoot(cls):
        cls.hero.shoot()
        # 子弹打到敌机让敌机从列表中消失
        ememyIndex = 0
        for i in cls.g_ememyList:
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top = i.y
            bulletIndex = 0
            for j in cls.hero.bulletList:
                bulletRect = pygame.Rect(j.image.get_rect())
                bulletRect.left = j.x
                bulletRect.top = j.y
                if enemyRect.colliderect(bulletRect):
                    # 判断敌机的宽度或者高度，来知道打中哪种类型的敌机
                    if enemyRect.width == 39:
                        cls.score += 1000  # 小中大飞机分别100,500,1000分
                    elif enemyRect.width == 60:
                        cls.score += 5000
                    elif enemyRect.width == 78:
                        cls.score += 10000
                    cls.g_ememyList.pop(ememyIndex)  # 敌机删除
                    cls.hero.bulletList.pop(bulletIndex)  # 打中的子弹删除
                bulletIndex += 1
            ememyIndex += 1

            # 判断游戏是否结束

    @classmethod
    def gameover(cls):
        heroRect = pygame.Rect(cls.hero.image.get_rect())
        heroRect.left = cls.hero.x
        heroRect.top = cls.hero.y
        for i in cls.g_ememyList:
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top = i.y
            if heroRect.colliderect(enemyRect):
                return True
        return False

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

    #定义一个糖果基类
class Candy(object):
	def __init__(self):
		#导弹间隔发射时间1s
		self.bulletSleepTime = 0.3
		self.lastShootTime = time.time()
		#存储导弹列表
		self.bulletList = []

	#描绘飞机
	def draw(self,screen):
		screen.blit(self.image,(self.x,self.y))

	def shoot(self):
		if time.time()-self.lastShootTime>self.bulletSleepTime:
			self.bulletList.append(Bullet(self.planeName,self.x+36,self.y))
			self.lastShootTime = time.time()

class Enemy(Candy):
    """docstring for Enemy"""

    def __init__(self, speed):
        super(Enemy, self).__init__()
        randomImageNum = random.randint(1, 3)
        planeImageName = 'Resources/enemy-' + str(randomImageNum) + '.png'
        self.image = pygame.image.load(planeImageName).convert()
        # 敌人飞机原始位置
        self.x = random.randint(20, 400)  # 敌机出现的位置任意
        self.y = 0
        self.planeName = 'enemy'
        self.direction = 'down'  # 用英文表示
        self.speed = speed  # 移动速度,这个参数现在需要传入

    def move(self):
        if self.direction == 'down':
            self.y += self.speed  # 飞机不断往下掉



# 定义main函数
def main():
    # 初始化pygame
    pygame.init()
    # 创建pygame显示层
    pygame.display.set_caption('board')
    # 创建一个窗口与背景图片一样大
    ScreenWidth, ScreenHeight = 360, 600
    screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), 0, 32)
    # 图片加载
    start = pygame.image.load("Resources/startone.png")  # 游戏开始图片
    background = pygame.image.load("Resources/bg_01.png").convert()  # 背景图片

    screen.blit(background, (0, 0))  # 不断覆盖，否则在背景上的图片会重叠
    pygame.display.update()  # 开始显示启动图片，直到有Enter键按下才会开始
    GameInit.waitForKeyPress()

    # 初始化变量
    snakePosition = [100,580]
    boardLength = 100
    pos = ''

    while True:
        screen.blit(background, (0, 0))  # 不断覆盖，否则在背景上的图片会重叠
        gameOverFont = pygame.font.SysFont('arial.ttf', 36)
        gameOverSurf = gameOverFont.render('Score:60', True, greyColour)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.midtop = (60, 10)
        screen.blit(gameOverSurf, gameOverRect)
        # 检测例如按键等pygame事件
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
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

        if (pos == 'right' and snakePosition[0] + boardLength < ScreenWidth):
            snakePosition[0] += 0.5
        elif (pos == 'left' and snakePosition[0] > 0):
            snakePosition[0] -= 0.5

        # 绘制pygame显示层

        # playSurface.fill(blackColour)
        pygame.draw.rect(screen,greyColour,Rect(snakePosition[0],snakePosition[1],boardLength,15))

        # 刷新pygame显示层
        pygame.display.flip()
        # 控制游戏速度
        # fpsClock.tick(5)

if __name__ == "__main__":
    main()

