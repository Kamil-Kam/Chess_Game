import pygame
import pygame as p
pygame.init()

font = p.font.SysFont('arial', 12, False, False)
a = '   pe7 e5'
text_object = font.render(a, True, p.Color('White'))
s = text_object.get_width()
print(s)