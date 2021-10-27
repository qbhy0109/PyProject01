import pygame
import sys
import time

SCREEN_X = 400
SCREEN_Y = 500
screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
pygame.display.set_caption('2048')

def show_text(string, position, color, height):
    font_obj = pygame.font.SysFont('simsunnsimsun', height)
    text_surface = font_obj.render(string, True, color)
    text_surface = text_surface.convert_alpha()
    screen.blit(text_surface, position)
    print(string)


if __name__ == '__main__':
    pygame.init()
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        show_text('Failed', (120, 200), (255, 0, 0), 50)
        show_text('Please Press Space to Continue', (30, 280), (255, 0, 0), 22)
        show_text('一个', (100, 100), (255, 0, 0), 35)
        time.sleep(1)
        pygame.display.update()