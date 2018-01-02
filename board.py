# !C:/Users/Administrator/Desktop/demo/python
# coding=utf-8

# 导入pygame库

import pygame, random, sys, time, os  # sys模块中的exit用于退出
from pygame.locals import *

# 定义一个道具基类
class Prop(object):
    # 定义一个画图方法
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 玩家类
class Role(Prop):

    def __init__(self):
        self.image = pygame.image.load('Resources/role.png').convert_alpha()
        # 玩家原始位置
        self.x = 300
        self.y = 360

    # 键盘控制圣诞老人
    def keyHandle(self, keyValue):
        if keyValue == 'left':
            self.x -= 1
        elif keyValue == 'right':
            self.x += 1


# 水果类
class Fruit(Prop):

    def __init__(self, speed):
        super(Fruit, self).__init__()
        fruitImage = 'Resources/fruit/' + str(random.randint(1, 4)) + '.png' # 随机选取4种水果的一种
        self.image = pygame.image.load(fruitImage).convert_alpha()
        # 定义水果原始位置
        self.x = random.randint(20, 640)  # 从任意位置掉落水果
        self.y = 0
        self.name = 'fruit'
        self.speed = speed  # 传入的移动速度

    def move(self):
        self.y += self.speed


# 定义炸弹
class Bomb(Prop):

    def __init__(self, speed):
        super(Bomb, self).__init__()
        self.image = pygame.image.load('Resources/prop/bomb.png').convert_alpha()
        # 炸弹原始位置
        self.x = random.randint(20, 640)  # 从任意位置掉落炸弹
        self.y = 0
        self.name = 'bomb'
        self.speed = speed  # 传入的移动速度

    def move(self):
        self.y += self.speed

# 定义星星
class Star(Prop):

    def __init__(self, speed):
        super(Star, self).__init__()
        self.image = pygame.image.load('Resources/prop/star.png').convert_alpha()
        # 炸弹原始位置
        self.x = random.randint(20, 640)  # 从任意位置掉落
        self.y = 0
        self.name = 'star'
        self.speed = speed  # 传入的移动速度

    def move(self):
        self.y += self.speed


class GameInit(object):
    """GameInit"""
    # 类属性
    gameLevel = 1  # 简单模式
    g_fruitList = []  # 前面加上g类似全局变量
    g_bombList = []  # 前面加上g类似全局变量
    score = 0  # 用于统计分数
    life = 3  # 用来统计生命
    role = object

    @classmethod
    def createFruit(cls, speed):
        cls.g_fruitList.append(Fruit(speed))

    @classmethod
    def createBomb(cls, speed):
        cls.g_bombList.append(Bomb(speed))

    @classmethod
    def createRole(cls):
        cls.role = Role()

    @classmethod
    def gameInit(cls):
        cls.createRole()

    @classmethod
    def rolePlaneKey(cls, keyValue):
        cls.role.keyHandle(keyValue)

    @classmethod
    def draw(cls, screen):
        delFruitList = []
        delBombList = []
        j = 0
        s = 0
        roleRect = pygame.Rect(cls.role.image.get_rect())
        roleRect.left = cls.role.x
        roleRect.top = cls.role.y
        for i in cls.g_fruitList:
            i.draw(screen)  # 画出水果
            fruitRect = pygame.Rect(i.image.get_rect())
            fruitRect.left = i.x
            fruitRect.top = i.y
            # 水果超过屏幕或者撞到就从列表中删除
            if roleRect.colliderect(fruitRect):
                # if fruitRect.width == 39:
                #     cls.score += 100  # 小中大分别100,500,1000分
                # if fruitRect.width == 60:
                #     cls.score += 500
                # if fruitRect.width == 78:
                #     cls.score += 1000

                if i.y <= 360:
                    cls.score += 100
                    delFruitList.append(j)
                    j += 1
            if i.y > 460:
                delFruitList.append(j)
                j += 1

        for m in delFruitList:
            del cls.g_fruitList[m]

        for i in cls.g_bombList:
            i.draw(screen)  # 画出炸弹
            fruitRect = pygame.Rect(i.image.get_rect())
            fruitRect.left = i.x
            fruitRect.top = i.y
            # 炸弹超过屏幕或者撞到就从列表中删除
            if i.y > 460:
                delBombList.append(s)
                s += 1

            if roleRect.colliderect(fruitRect):
                if i.y <= 360:
                    time.sleep(0.3)

                    cls.life -= 1
                    delBombList.append(s)
                    s += 1
                    print(cls.life)

        for m in delBombList:
            del cls.g_bombList[m]

        cls.role.draw(screen)  # 画出圣诞老人位置

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
    def drawText(text, font, surface, color, x, y):
        # 参数1：显示的内容 |参数2：是否开抗锯齿，True平滑一点|参数3：字体颜色|参数4：字体背景颜色
        content = font.render(text, True, color)
        contentRect = content.get_rect()
        contentRect.left = x
        contentRect.top = y
        surface.blit(content, contentRect)


def main():
    # 初始化pygame
    pygame.init()
    # 创建一个窗口与背景图片一样大
    ScreenWidth, ScreenHeight = 680, 460
    FruitSleepTime = [2, 1.4, 1]
    lastFruitTime = 0


    pos = ''
    screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), 0, 32)
    pygame.display.set_caption('圣诞老人接水果')
    # 参数1：字体类型，例如"arial"  参数2：字体大小
    font_gameover = pygame.font.SysFont("arial", 64)
    font1 = pygame.font.SysFont("arial", 24)
    font2 = pygame.font.SysFont("arial", 30)
    # 记录游戏开始的时间
    startTime = time.time()
    # 背景图片加载并转换成图像
    background = pygame.image.load("Resources/bg.jpg").convert()  # 背景图片
    gameover = pygame.image.load("Resources/gameover.jpg").convert()  # 游戏结束图片
    start = pygame.image.load("Resources/start.jpg")  # 游戏开始图片
    heartIcon = pygame.image.load("Resources/heart.png")
    timeIcon = pygame.image.load("Resources/time.png")
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

        screen.blit(background, (0, 0))  # 不断覆盖，否则在背景上的图片会重叠
        screen.blit(heartIcon, (400, 10))  # 生命图标
        screen.blit(timeIcon, (490, 10))  # 时间条
        GameInit.drawText('%s' % (GameInit.life), font2, screen, (10, 100, 200), 450, 10)
        GameInit.drawText('score:%s' % (GameInit.score), font1, screen, (10, 100, 200), 30, 15)
        if int(GameInit.score) < int(historyscore):
            GameInit.drawText('best:%s' % (historyscore), font1, screen, (10, 100, 200), 30, 35)
        else:
            GameInit.drawText('best:%s' % (GameInit.score), font1, screen, (10, 100, 200), 30, 35)
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
            GameInit.rolePlaneKey('right')
        elif (pos == 'left'):
            GameInit.rolePlaneKey('left')

        interval = time.time() - startTime
        # easy模式
        if interval < 10:
            if time.time() - lastFruitTime >= FruitSleepTime[0]:
                GameInit.createFruit(0.8)  # 传入的参数是speed
                GameInit.createBomb(0.5)
                lastFruitTime = time.time()
        # middle模式
        elif interval >= 10 and interval < 30:
            if time.time() - lastFruitTime >= FruitSleepTime[1]:
                GameInit.createFruit(1)
                GameInit.createBomb(0.5)
                lastFruitTime = time.time()
        # hard模式
        elif interval >= 30:
            if time.time() - lastFruitTime >= FruitSleepTime[2]:
                GameInit.createFruit(1.2)
                GameInit.createBomb(0.5)
                lastFruitTime = time.time()
        GameInit.setXY()
        GameInit.draw(screen)  # 描绘类的位置
        pygame.display.update()  # 不断更新图片
        if GameInit.gameover():
            time.sleep(1)  # 睡1s时间,让玩家看到与炸弹相撞的画面
            screen.blit(gameover, (0, 0))
            GameInit.drawText('score:%s' % (GameInit.score), font_gameover, screen, (255, 255, 255), 70, 240)
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
