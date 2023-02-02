import os
import tkinter as tk

from math import cos, tan
from pygame import *

init()

# Setup display

root = tk.Tk()

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

HEIGHT = 600
WIDTH = 1200

win_x = screen_width // 2 - WIDTH // 2
win_y = screen_height // 2 - HEIGHT // 2

os.environ["SDL_VIDEO_WINDOW_POS"] = str(win_x) + ',' + str(win_y)
win = display.set_mode((WIDTH, HEIGHT))  # main window
display.set_caption("Geometry-Dash")

bg = image.load("Images/background.jpg")
bg_rect = bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

ground = Surface((WIDTH * 2, HEIGHT * 3 // 10))
ground_rect = ground.get_rect(bottomleft=(0, HEIGHT))
ground_img = transform.scale(image.load("Images/ground.jpg"), (ground_rect.w // 2, ground_rect.h))
ground_img_rect = ground_img.get_rect(topleft=(0, 0))
ground.blit(ground_img, ground_img_rect)
ground_img_rect = ground_img.get_rect(topleft=(ground_rect.centerx, 0))
ground.blit(ground_img, ground_img_rect)


def move_ground(rect):
    """Move the ground each frame"""

    rect.x -= 10

    if rect.centerx == 0:
        rect.left = 0


class Icon:
    """The square to move"""

    def init(self, img_location, bottom):
        self.size = 100
        self.image = transform.scale(image.load(img_location), (self.size, self.size))
        self.rect = self.image.get_rect(bottomleft=(self.size * -1, bottom))
        self.fixed_centerx = WIDTH * 2 // 10
        self.mincentery = bottom - self.size // 2
        self.yspeed = 10

    def fall(self):
        self.rect.centery += self.yspeed

    def jump(self):
        self.rect.centery -= self.yspeed
        # self.image = transform.rotate(self.image, -9/2)
        # self.rect = self.image.get_rect(center = (self.fixed_centerx, self.rect.centery))

    def move(self):
        self.rect.x += 10


class Spike:
    pass


icon = Icon("Images/icon.png", HEIGHT - ground_img_rect.h)

# Game settings

falling = False
jumping = False
max_height = 0

# Setup game loop

FPS = 60
clock = time.Clock()
run = True

while run:
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                jumping = True
                max_height = icon.rect.centery - 2 * icon.size

    if icon.rect.x < icon.fixed_centerx:
        icon.move()

    if falling:
        icon.fall()

    if icon.rect.centery >= icon.mincentery:
        falling = False

    if jumping:
        icon.jump()

    if icon.rect.centery <= max_height:
        jumping = False
        falling = True

    move_ground(ground_rect)

    win.blit(bg, bg_rect)
    win.blit(ground, ground_rect)
    win.blit(icon.image, icon.rect)
    display.update()

quit()