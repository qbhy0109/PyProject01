import pygame
import sys
import random
import time


SCREEN_X = 400
SCREEN_Y = 500
BOX_SIZE = 75
BOX_GAP = 6
SCREEN_LEFT = 35
SCREEN_TOP = 80
score = 0

# 各种不同的RGB色彩混合，完全按照原版2048仿制
COLOR = {'surface': (255, 255, 255),
         'black': (0, 0, 0),
         'gray': (222, 222, 222),
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
         2048: (225, 187, 0)}

board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
pygame.display.set_caption('2048')

class BOX:
    def __init__(self, position, color, text):
        self.position = position
        self.color = color
        self.text = text

    def render(self):
        x, y = self.position
        pygame.draw.rect(screen, self.color, (x, y, BOX_SIZE, BOX_SIZE))

        font_obj = pygame.font.SysFont('arial', 35)
        text_surface = font_obj.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + BOX_SIZE//2, y + BOX_SIZE//2)
        screen.blit(text_surface, text_rect)


def show_box():

    y = SCREEN_TOP + BOX_GAP
    for i in range(4):
        x = SCREEN_LEFT + BOX_GAP
        for j in range(4):
            idx = board[i][j]
            if idx == 0:
                text = ''
            else:
                text = str(idx)
            color = COLOR[idx]
            position = x, y
            box = BOX(position, color, text)
            box.render()
            x = x + BOX_SIZE + BOX_GAP
        y = y + BOX_SIZE + BOX_GAP


def show_text(string, position, color, height):
    font_obj = pygame.font.SysFont('simsunnsimsun', height)
    text_surface = font_obj.render(string, True, color)
    text_surface = text_surface.convert_alpha()
    screen.blit(text_surface, position)


def show_score(score):
    show_text('SCORE:'+str(score), (130, 20), (255, 0, 0), 35)


def make_number():
    number = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                number.append((i,j))
    try:
        m = random.choice(number)
        number.remove(m)
        value = random.uniform(0, 1)
        if value > 0.1:
            value = 2
        else:
            value = 4
        board[m[0]][m[1]] = value
    except:
        pass


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


def board_init():
    global board
    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
    for x in range(2):
        make_number()


def main():

    pygame.init()
    boarded = board
    board_init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left()
                    if board != boarded:
                        make_number()
                        boarded = board
                elif event.key == pygame.K_RIGHT:
                    right()
                elif event.key == pygame.K_UP:
                    up()
                elif event.key == pygame.K_DOWN:
                    down()




                if win():
                    show_text('Winning!!!', (100, 200), (255, 0, 0), 50)
                    show_text('Please Press Space to Continue', (30, 280), (255, 0, 0), 22)
                    time.sleep(3)
                    if event.key == pygame.K_SPACE:
                        return main()
                if is_over():
                    show_text('Failed', (120, 200), (255, 0, 0), 50)
                    show_text('Please Press Space to Continue', (30, 280), (255, 0, 0), 22)
                    time.sleep(3)
                    if event.key == pygame.K_SPACE:
                        return main()

        background = pygame.image.load('photo1_end.jpg').convert()
        background = pygame.transform.scale(background, (400, 500))

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, COLOR['gray'], (35, 80, 330, 330))
        show_box()
        show_score(score)
        show_text('提示：按上下左右键进行游戏', (30, 430), COLOR['black'], 20)
        show_text('游戏结束按空格重新开始', (30, 450), COLOR['black'], 20)

        pygame.display.update()


if __name__ == '__main__':
    main()
