# -*- coding=utf-8 -*-
import random
import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

pygame.init()
screencaption = pygame.display.set_caption('first pygame')
screen = pygame.display.set_mode((400, 400))  # 设置400*400窗口

snake_x = random.randint(0, 9) * 40 + 20
snake_y = random.randint(0, 9) * 40 + 20


def get_bean_pos():
    return random.randint(0, 9) * 40 + 20, random.randint(0, 9) * 40 + 20


yellow = 255, 255, 0

bean_x, bean_y = get_bean_pos()

diff_ticks = 300  # 移动一次蛇头的事件，单位毫秒
ticks = pygame.time.get_ticks()
ticks += diff_ticks

# dire = random.randint(0,3) # 假设0、1、2、3分别代表方向左、右、上、下
if snake_x < 5:
    dire = 1  # 往右移动
else:
    dire = 0  # 往左移动

body_y = snake_y
if dire == 0:  # 向左移动
    if snake_x + 40 < 400:
        body_x = snake_x + 40
    else:  # 身体不能放右侧了，只能往上下方向放
        if snake_y > 200:
            body_x = snake_x
            body_y -= 40
        else:
            body_x = snake_x
            body_y += 40
else:  # 向右移动
    if snake_x - 40 > 0:
        body_x = snake_x - 40
    else:  # 身体不能放左侧了，只能往上下方向放
        if snake_y > 200:
            body_x = snake_x
            body_y -= 40
        else:
            body_x = snake_x
            body_y += 40


def set_snake_next_pos(snake_x, snake_y):
    if dire == 0:
        if snake_x - 40 > 0:
            snake_x -= 40
    if dire == 1:
        if snake_x + 40 < 400:
            snake_x += 40
    if dire == 2:
        if snake_y - 40 > 0:
            snake_y -= 40
    if dire == 3:
        if snake_y + 40 < 400:
            snake_y += 40
    return snake_x, snake_y


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if dire != 0 and dire != 1 and snake_x - 40 > 0:  # 和当前方向不是同方向或反方向并且可以左移
                    dire = 0
            if event.key == K_RIGHT:
                if dire != 0 and dire != 1 and snake_x + 40 < 400:  # 和当前方向不是同方向或反方向并且可以右移
                    dire = 1
            if event.key == K_UP:
                if dire != 2 and dire != 3 and snake_y - 40 > 0:  # 和当前方向不是同方向或反方向并且可以上移
                    dire = 2
            if event.key == K_DOWN:
                if dire != 2 and dire != 3 and snake_y + 40 < 400:  # 和当前方向不是同方向或反方向并且可以下移
                    dire = 3

    screen.fill((0, 0, 255))  # 将界面设置为蓝色

    for x in range(0, 400, 40):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, 400), 1)
    for y in range(0, 400, 40):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (400, y), 1)

    pygame.draw.circle(screen, yellow, [snake_x, snake_y], 20, 2)
    pygame.draw.rect(screen, yellow, [body_x - 20, body_y - 20, 40, 40], 5)

    pygame.draw.circle(screen, yellow, [bean_x, bean_y], 10, 10)

    pygame.display.update()  # 必须调用update才能看到绘图显示

    if pygame.time.get_ticks() >= ticks:
        body_x = snake_x
        body_y = snake_y
        snake_x, snake_y = set_snake_next_pos(snake_x, snake_y)
        ticks += diff_ticks




