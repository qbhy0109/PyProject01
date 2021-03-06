# 本程序用到的一些库
# import os
import random
import pygame
from sys import exit
from copy import deepcopy
from pygame.locals import *

pygame.init()
FPS = 5
b4 = "button4.jpg"
b5 = "button5.jpg"
b6 = "button6.jpg"
# folder = r'C:\Users\longlong\Music'
# musics = [folder + '\\' + music for music in os.listdir(folder)
#          if music.endswith('.mp3')]
# total = len(musics)
pygame.init()

board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

box_size = 100  # 每个小方格
box_gap = 5  # 每个小方格与每个小方格之间的间距
top_of_screen = 100  # 格子到窗口顶端的距离
bottom_of_screen = 20  # 格子到窗口底端的距离
left_of_screen = 50  # 格子到窗口左端的距离
screen_width = 520  # 游戏界面的宽
screen_height = 600  # 游戏界面的高度
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)  # 初始化一个准备显示的窗口或屏幕
pygame.display.set_caption("My2048")  # 设置游戏窗口标题
background = pygame.image.load('background3.jpg').convert()  # 设置游戏背景图
high_score_name = "test.txt"
score = 0  # 得分
tmpScore = 0
high_score = 0

'''
def play_music():  # 此函数的功能是播放音乐
    if not pygame.mixer.music.get_busy():
        nextMusic = random.choice(musics)
        pygame.mixer.music.load(nextMusic)
        pygame.mixer.music.play(1)
    else:
        time.sleep(1)
'''

class Button(object):  # 此类是一个自定义好的按钮类，用在游戏中出现的各种按钮
    def __init__(self, position, fileName, sizex, sizey):  # 初始化该按钮，包括加载图片，初始位置，按钮大小
        self.imageUp = pygame.image.load(fileName).convert_alpha()
        self.position = position
        self.imageUp = pygame.transform.scale(self.imageUp, (sizex, sizey))
        screen.blit(self.imageUp, self.position)

    def isOver(self):  # 判断鼠标是否放在该按钮上
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageUp.get_size()

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y

    def render(self):  # 判断是否要重新开始一局游戏
        global score
       # w, h = self.imageUp.get_size()
       # x, y = self.position
        if self.isOver() == True:
            score = 0
            draw_box(0)
            init_board()


class Box:
    def __init__(self, topleft, text, color):
        self.topleft = topleft
        self.text = text
        self.color = color

    def render(self, surface):
        x, y = self.topleft
        pygame.draw.rect(surface, self.color, (x, y, box_size, box_size), 0)
        text_height = 35
        font_obj = pygame.font.SysFont("arial", text_height)
        text_surface = font_obj.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + 50, y + 50)
        surface.blit(text_surface, text_rect)


def load_data():  # 读取本地txt文件中的本机最高得分
    with open(high_score_name, "r") as f:
        high = int(f.read())
        return high


board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

def draw_box(type):  # 绘制游戏棋盘界面，用一个4x4的列表表示
    global board
    if type == 0:
        pass

    colors = {  # 各种不同的RGB色彩混合，完全按照原版2048仿制
        0: (205, 193, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 98),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (225, 187, 0)
    }
    x, y = left_of_screen, top_of_screen
    size = 425
    pygame.draw.rect(screen, (187, 173, 160), (x, y, size, size))
    x, y = x + box_gap, y + box_gap
    for i in range(4):
        for j in range(4):
            idx = board[i][j]
            if idx == 0:
                text = ""
            else:
                text = str(idx)
            if idx > 2048:
                idx = 2048
            color = colors[idx]
            box = Box((x, y), text, color)
            box.render(screen)
            x += box_size + box_gap
        x = left_of_screen + box_gap
        y += top_of_screen + box_gap


def set_random_number():  # 此函数的功能是用户每移动一步后在数字0处随机产生一个2或4
    num = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                num.append((i, j))
    m = random.choice(num)
    num.remove(m)
    value = random.uniform(0, 1)
    if value < 0.1:  # 产生4的概率要小一点
        value = 4
    else:
        value = 2
    board[m[0]][m[1]] = value


def init_board():  # 游戏开始时初始化棋盘：随机产生两个2/4
    for i in range(2):
        set_random_number()


def combinate(L):  # 此函数的功能是进行方块的合并原理，是本程序的重难点所在
    global score
    ans = [0, 0, 0, 0]
    num = []
    for i in L:
        if i != 0:  # 把本行中所有的数字放到列表num中去
            num.append(i)
    length = len(num)
    if length == 4:  # 本行中有4个数字
        if num[0] == num[1]:  # case1
            ans[0] = num[0] + num[1]
            score += ans[0]
            if num[2] == num[3]:
                ans[1] = num[2] + num[3]
                score += ans[1]
            else:
                ans[1] = num[2]
                ans[2] = num[3]
        elif num[1] == num[2]:  # case2
            ans[0] = num[0]
            ans[1] = num[1] + num[2]
            ans[2] = num[3]
            score += ans[1]
        elif num[2] == num[3]:  # case3
            ans[0] = num[0]
            ans[1] = num[1]
            ans[2] = num[2] + num[3]
            score += ans[2]
        else:  # case4 没有能合并的数字
            for i in range(length):
                ans[i] = num[i]
    elif length == 3:  # 本行中有3个数字
        if num[0] == num[1]:  # case 1
            ans[0] = num[0] + num[1]
            ans[1] = num[2]
            score += ans[0]
        elif num[1] == num[2]:  # case 2
            ans[0] = num[0]
            ans[1] = num[1] + num[2]
            score += ans[1]
        else:  # case 3 没有能合并的数字
            for i in range(length):
                ans[i] = num[i]
    elif length == 2:  # 本行中有2个数字
        if num[0] == num[1]:  # case 1
            ans[0] = num[0] + num[1]
            score += ans[0]
        else:  # case 2 没有能合并的数字
            for i in range(length):
                ans[i] = num[i]
    elif length == 1:
        ans[0] = num[0]
    else:
        pass
    return ans


def left():  # 用户按下左键进行的移动
    for i in range(4):
        temp = combinate(board[i])
        for j in range(4):
            board[i][j] = temp[j]


def right():  # 用户按下右键进行的移动
    for i in range(4):
        temp = combinate(board[i][::-1])
        for j in range(4):
            board[i][3 - j] = temp[j]


def up():  # 用户按下上键进行的移动
    for i in range(4):
        to_comb = []
        for j in range(4):
            to_comb.append(board[j][i])
        temp = combinate(to_comb)
        for k in range(4):
            board[k][i] = temp[k]


def down():  # 用户按下下键进行的移动
    for i in range(4):
        to_comb = []
        for j in range(4):
            to_comb.append(board[3 - j][i])
        temp = combinate(to_comb)
        for k in range(4):
            board[3 - k][i] = temp[k]


def write(msg="Winning!!!", color=(255, 255, 0), height=14):  # 在屏幕上打印字体
    # path = 'C:/Windows/Fonts/simhei.ttf'
    myfont = pygame.font.SysFont("simsunnsimsun", height)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext


def win():  # 判断当前是否胜利
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:  # 有2048，肯定是胜利了
                return True
    return False


def is_over():  # 判断当前是否失败
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:  # 有0，还有空白处，肯定不算失败
                return False
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1]:  # 左右有相同的字母，还能够合并，肯定不算失败
                return False
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i + 1][j]:  # 上下有相同的字母，还能够合并，肯定不算失败
                return False
    return True  # 失败了


def game_skill():  # 游戏技巧介绍
    button_back = Button((left_of_screen + 140, 480), "button_back.jpg", 130, 50)
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.isOver() == True:
                    return
            pygame.display.update()
            rect = pygame.draw.rect(screen, (251, 248, 241), (10, 10, 500, 580))
            screen.blit(write("1、简单点来说就是尽量不要向上。", height=30, color=(119, 110, 101)), (30, 165))
            screen.blit(write("滑动就可以了,尽量用左下右三个", height=30, color=(119, 110, 101)), (30, 195))
            screen.blit(write("键游戏，让大的方块尽量沉在底部", height=30, color=(119, 110, 101)), (30, 225))
            screen.blit(write("2、数越来越大以后，较大的数要", height=30, color=(119, 110, 101)), (30, 255))
            screen.blit(write("依次靠着这个。让一行中数字顺序", height=30, color=(119, 110, 101)), (30, 285))
            screen.blit(write("紧邻排列。不要总是急于清理桌面。", height=30, color=(119, 110, 101)), (30, 315))
            screen.blit(write("3、因为尽量不向上滑动，所以大的", height=30, color=(119, 110, 101)), (30, 345))
            screen.blit(write("数必然在底下。然后就是不要图快。", height=30, color=(119, 110, 101)), (30, 375))
            screen.blit(write("4、当游戏进行不下去时，NewGame", height=30, color=(119, 110, 101)), (30, 405))
            screen.blit(write("键点击重新开始，祝你玩的愉快。", height=30, color=(119, 110, 101)), (30, 435))
            button_back = Button((left_of_screen + 140, 480), "button_back.jpg", 130, 50)
            screen.blit(write("2048", height=100, color=(119, 110, 101)),
                        (left_of_screen + 110, left_of_screen // 2))

def game_introduce():  # 游戏玩法介绍
    button_back = Button((left_of_screen + 140, 480), "button_back.jpg", 130, 50)
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.isOver() == True:
                    return
            pygame.display.update()
            rect = pygame.draw.rect(screen, (251, 248, 241), (10, 10, 500, 580))
            screen.blit(write("游戏的规则很简单", height=30, color=(119, 110, 101)), (135, 165))
            screen.blit(write("需要控制所有方块", height=30, color=(119, 110, 101)), (135, 195))
            screen.blit(write("向同一个方向运动", height=30, color=(119, 110, 101)), (135, 225))
            screen.blit(write("两个相同数字方块", height=30, color=(119, 110, 101)), (135, 255))
            screen.blit(write("撞在一起之后会合", height=30, color=(119, 110, 101)), (135, 285))
            screen.blit(write("并成为他们的加和", height=30, color=(119, 110, 101)), (135, 315))
            screen.blit(write("之后会新产生一个", height=30, color=(119, 110, 101)), (135, 345))
            screen.blit(write("2或4当拼凑得到了", height=30, color=(119, 110, 101)), (135, 375))
            screen.blit(write("2048游戏就算胜利", height=30, color=(119, 110, 101)), (135, 405))
            button_back = Button((left_of_screen + 140, 480), "button_back.jpg", 130, 50)
            screen.blit(write("2048", height=100, color=(119, 110, 101)),
                        (left_of_screen + 110, left_of_screen // 2))


def game_view_page0():  # 游戏欢迎界面，这里实现了一个动画功能：两排大小颜色不同的“2048小游戏”绕屏幕中心进行旋转
    FPS = 5
    BLACK = (0, 0, 0)
    BROWN = (187, 173, 160)
    WHITE = (255, 255, 255)
    BGCOLOR = BROWN
    titleFont = pygame.font.Font(r'C:\Windows\Fonts\simkai.ttf', 100)
    titleSurf1 = titleFont.render('2048小游戏', True, BLACK)
    titleSurf2 = titleFont.render('2048小游戏', True, WHITE)
    degrees1 = 0
    degrees2 = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYUP:
                return
        screen.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (screen_width / 2, screen_height / 2 - 50)
        screen.blit(rotatedSurf1, rotatedRect1)
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (screen_width / 2, screen_height / 2 - 50)
        screen.blit(rotatedSurf2, rotatedRect2)
        screen.blit(write("点击鼠标左键进入游戏", height=30, color=(255, 255, 255)),
                    (left_of_screen + 60, left_of_screen // 2 + 450))
        pygame.display.update()
        FPSCLOCK.tick(10)
        degrees1 += 3
        degrees2 += 5


def game_start_page():  # 游戏开始界面
    # 加载背景图片
    screen.blit(background, (0, 0))
    # 创建几个自定义的按钮
    button4 = Button((left_of_screen + 110, 150), b4, 200, 80)
    button5 = Button((left_of_screen + 110, 270), b5, 200, 80)
    button6 = Button((left_of_screen + 110, 390), b6, 200, 80)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button4.isOver() == True:  # 如果按下的是button4,即开始游戏
                    return
                elif button5.isOver() == True:  # 如果按下的是button5，即游戏玩法介绍
                    game_introduce()
                    screen.blit(background, (0, 0))
                    button4 = Button((left_of_screen + 110, 150), b4, 200, 80)
                    button5 = Button((left_of_screen + 110, 270), b5, 200, 80)
                    button6 = Button((left_of_screen + 110, 390), b6, 200, 80)
                elif button6.isOver() == True:  # 如果按下的是button6，即游戏技巧介绍
                    game_skill()
                    screen.blit(background, (0, 0))
                    button4 = Button((left_of_screen + 110, 150), b4, 200, 80)
                    button5 = Button((left_of_screen + 110, 270), b5, 200, 80)
                    button6 = Button((left_of_screen + 110, 390), b6, 200, 80)
            screen.blit(write("2048", height=100, color=(119, 110, 101)),
                        (left_of_screen + 110, left_of_screen // 2))
            pygame.display.update()


def main():
    # play_music()注释掉了，播放音乐会导致游戏很卡
    global FPSCLOCK, score, high_score, tmpScore, board
    flag = False
    flag2 = False
    FPSCLOCK = pygame.time.Clock()
    game_view_page0()  # 游戏欢迎界面
    game_start_page()  # 游戏主菜单界面
    b = [[0, 0, 0, 0],  # b是用来记录每次用户移动前一步的棋盘状态的，可以用于实现“回到上一步”功能
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    screen.blit(background, (0, 0))
    init_board()
    newboard = deepcopy(board)
    gameover = is_over()
    draw_box(1)
    button = Button((left_of_screen + 210, left_of_screen // 2 + 5), "button3.jpg", 100, 60)
    screen.blit(write("2048", height=60, color=(119, 110, 101)),
                (left_of_screen, left_of_screen // 2))
    high_score = load_data()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):  # 用户如果按了ESC，退出
                pygame.quit()
                exit()
            elif not gameover:  # 如果当前游戏还没有失败（棋盘上还有空格，即数字0）
                if win() == True:  # 如果当前赢了（拼出来了数字2048）
                    screen.blit(write("You win!", height=40, color=(119, 110, 101)),  # 屏幕上打印“You win!”
                                (left_of_screen + 160, screen_height // 2 - 30))
                elif event.type == KEYUP and event.key == K_UP:  # 用户按了 up 键
                    tmpScore = score
                    flag = False
                    up()
                elif event.type == KEYUP and event.key == K_DOWN:  # 用户按了 down 键
                    tmpScore = score
                    flag = False
                    down()
                elif event.type == KEYUP and event.key == K_LEFT:  # 用户按了 left 键
                    tmpScore = score
                    flag = False
                    left()
                elif event.type == KEYUP and event.key == K_RIGHT:  # 用户按了 right 键
                    tmpScore = score
                    flag = False
                    right()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 用户点击了鼠标，也就是用户按下了重新开始的按钮
                    button.render()  # 重新开始一局游戏
                    flag = False  # 初始化各个数值
                    flag2 = True
                elif event.type == KEYUP and event.key == K_SPACE:  # 用户按了 space 打算回到上一步
                    if flag == False:
                        board = deepcopy(b)
                        score = tmpScore
                        flag = True
                if newboard != board:
                    b = deepcopy(newboard)
                    if flag == False and flag2 == False:
                        set_random_number()
                    flag2 = False
                    newboard = deepcopy(board)
                    draw_box(1)
                gameover = is_over()
            else:  # 否则判定用户本局游戏失败
                screen.blit(write("Game over!", height=40, color=(119, 110, 101)),  # 打印失败信息
                            (left_of_screen + 140, screen_height // 2 - 40))
                if score > high_score:  # 如果用户的分数比本机最高得分高
                    screen.blit(write("New record!", height=40, color=(119, 110, 101)),  # 提示用户刷新了记录
                                (left_of_screen + 140, screen_height // 2 + 10))
                    high_score = score
                    with open(high_score_name, "w") as f:
                        f.write(str(high_score))  # 用新的得分覆盖原有的最高得分
                if event.type == pygame.MOUSEBUTTONDOWN:  # 用户点击了鼠标，也就是用户按下了重新开始的按钮
                    gameover = False
                    score = 0
                    tmpScore = 0  # 初始化各个数值
                    button.render()  # 重新开始一局游戏
                    flag2 = True

        pygame.display.update()

        rect1 = pygame.draw.rect(screen, (187, 173, 160),
                                 (left_of_screen + 120, left_of_screen // 2 + 5, 80, 60))
        rect2 = pygame.draw.rect(screen, (187, 173, 160),
                                 (left_of_screen + 320, left_of_screen // 2 + 5, 105, 60))
        screen.blit(write("score:", height=28, color=(255, 255, 255)),
                    (left_of_screen + 125, left_of_screen // 2 + 5))
        screen.blit(write("best:", height=30, color=(255, 255, 255)),
                    (left_of_screen + 340, left_of_screen // 2 + 5))
        text1 = write(str(score), height=30, color=(255, 255, 255))
        text2 = write(str(high_score), height=30, color=(255, 255, 255))
        text_rect = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect.center = (left_of_screen + 160, left_of_screen // 2 + 50)
        text_rect2.center = (left_of_screen + 370, left_of_screen // 2 + 50)
        screen.blit(text1, text_rect)
        screen.blit(text2, text_rect2)


if __name__ == "__main__":
    main()
