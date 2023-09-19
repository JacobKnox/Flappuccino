#!/usr/bin/env python3
# Tells Unix operating systems to run with Python3 when it gets executed

import pygame
import sys
import time
import random
import colorsys
import math
import pygame.display as Display
import asyncio
from pygame.locals import *
from pygame.mixer import Sound
from pygame.font import Font
from pygame.image import load as Image
from player import Player
from imageasset import ImageAsset
from button import Button
from bean import Bean
from utils import *
from PIL import Image as img

# initialize the game
pygame.init()

# set the display
Display.set_caption('Flappuccino')
Display.set_icon(Bean.sprite)
display = Display.set_mode((640, 480), pygame.RESIZABLE | pygame.SCALED, 32)
pic = pygame.surface.Surface((50, 50))
pic.fill((255, 100, 200))

player = Player()

# get fonts
font = Font('data/fonts/font.otf', 100)
font_small = Font('data/fonts/font.otf', 32)
font_20 = Font('data/fonts/font.otf', 20)

# get some images
shop = ImageAsset('data/gfx/shop.png')
shop_bg = ImageAsset('data/gfx/shop_bg.png')
retry_button = ImageAsset('data/gfx/retry_button.png')
logo = ImageAsset('data/gfx/logo.png')
temp_title_bg = img.open('data/gfx/bg.png')
mode = temp_title_bg.mode
size = temp_title_bg.size
data = temp_title_bg.tobytes()
title_bg = pygame.image.fromstring(data, size, mode)
title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
shadow = ImageAsset('data/gfx/shadow.png')
indicators = ['data/gfx/flap_indicator.png',
              'data/gfx/speed_indicator.png', 'data/gfx/beanup_indicator.png']

# sounds
if ['win64', 'win32', 'win', 'linux'].__contains__(sys.platform):
    sound_ext = '.wav'
else:
    sound_ext = '-pybag.ogg'
flapfx = pygame.mixer.Sound("data/sfx/flap" + sound_ext)
upgradefx = pygame.mixer.Sound("data/sfx/upgrade" + sound_ext)
beanfx = pygame.mixer.Sound("data/sfx/bean" + sound_ext)
deadfx = pygame.mixer.Sound("data/sfx/dead" + sound_ext)

# colors
WHITE = (255, 255, 255)  # constant


def start():
    global bean_multiplier, beans, buttons, last_time, clicked, jump, dt, mouse_x, mouse_y, scroll
    last_time = time.time()
    clicked = False
    jump = False
    scroll = True
    dt = 0
    bean_multiplier = 5
    beans = []
    buttons = []
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.reset()
    # adding three buttons
    for i in range(3):
        buttons.append(Button(i, indicators[i]))
    buttons[2].set_price(30)
    # getting 5 beans
    for i in range(5):
        beans.append(Bean(random.randrange(0, display.get_width() -
                     Bean().sprite.get_width()), i * -200 - player.position.y))
    Sound.play(flapfx)


def func_one(toggle: bool = True) -> None:
    global dt, last_time, mouse_x, mouse_y, clicked, jump
    # calculate the change in time (dt)
    dt = (time.time() - last_time) * 60
    # save the current time
    last_time = time.time()
    if (toggle):
        # resetting clicked and jump flags to false
        clicked = False
        jump = False
        # get the position of the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
    event_handler()


def event_handler() -> None:
    global jump, clicked, display, temp_title_bg, title_bg
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            jump = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
        if clicked and mouse_y < display.get_height() - 90:
            jump = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            for o in bg:
                o.resize(event.size)
                display.blit(o.sprite, (0, o.position))
            temp_title_bg = temp_title_bg.resize(event.size)
            mode = temp_title_bg.mode
            size = temp_title_bg.size
            data = temp_title_bg.tobytes()
            title_bg = pygame.image.fromstring(data, size, mode)
            display = pygame.display.set_mode(
                event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)
            display.blit(pygame.transform.scale(
                title_bg, display.get_rect().size), (0, 0))
            display.fill((231, 205, 183))
            display.blit(logo.sprite, (display.get_width()/2 - logo.get_width()/2,
                         display.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))
            display.blit(retry_button.sprite, (display.get_width(
            )/2 - retry_button.get_width()/2, (3 * display.get_height())/4 - retry_button.get_height()/2))
            start_message = font_small.render("START", True, (0, 0, 0))
            display.blit(start_message, (display.get_width()/2 - start_message.get_width() /
                         2, (3 * display.get_height())/4 - start_message.get_height()/2))
            shop.resize((event.size[0], shop.get_height()))
            display.blit(shop_bg.sprite, (0, 0))
            pygame.display.flip()


async def main() -> None:
    global clicked, bean_multiplier, beans, scroll, bg
    start()

    # creating a list of backgrounds, with each index being an object
    bg = [ImageAsset(), ImageAsset(), ImageAsset()]
    # startingHeight = 100 (the initial y position of the player)
    starting_height = player.position.y

    # splash screen
    splash_screen_timer = 0
    while splash_screen_timer < 100:
        func_one(False)
        splash_screen_timer += dt
        display.fill((231, 205, 183))
        # fill the start message on the top of the game
        start_message = font_small.render("POLYMARS", True, (171, 145, 123))
        display.blit(start_message, (display.get_width()/2 - start_message.get_width() /
                     2, (3 * display.get_height())/4 - start_message.get_height()/2))
        # update display
        Display.update()
        await asyncio.sleep(0)
        # wait for 10 seconds
        pygame.time.delay(10)

    # title screen
    title_screen = True
    Sound.play(flapfx)
    while title_screen:
        func_one()
        # so the user clicked, and by any change the mouse's position was on the buttons
        if (clicked and check_collisions(mouse_x, mouse_y, 3, 3, display.get_width()/2 - retry_button.get_width()/2, (3 * display.get_height())/4 - retry_button.get_height()/2, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            title_screen = False
            Sound.play(upgradefx)

        display.fill(WHITE)
        display.blit(title_bg, (0, 0))
        display.blit(shadow.sprite, (0, 0))
        display.blit(logo.sprite, (display.get_width()/2 - logo.get_width()/2,
                     display.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))
        display.blit(retry_button.sprite, (display.get_width(
        )/2 - retry_button.get_width()/2, (3 * display.get_height())/4 - retry_button.get_height()/2))
        start_message = font_small.render("START", True, (0, 0, 0))
        display.blit(start_message, (display.get_width()/2 - start_message.get_width() /
                     2, (3 * display.get_height())/4 - start_message.get_height()/2))

        Display.update()
        await asyncio.sleep(0)
        pygame.time.delay(10)

    # the main game loop
    while True:
        func_one()

        cam_offset = -player.position.y + \
            (display.get_height() - player.current_sprite.get_size()[1])/2
        if (cam_offset <= 0):
            if (not player.dead):
                player.kill(deadfx)
            scroll = False
            cam_offset = 0

        display.fill(WHITE)
        for o in bg:
            o.set_sprite(((player.position.y/50) % 100) / 100)
            display.blit(o.sprite, (0, o.position))
        color = colorsys.hsv_to_rgb(
            ((player.position.y/50) % 100) / 100, 0.5, 0.5)
        current_height_marker = font.render(
            str(player.height), True, (color[0]*255, color[1]*255, color[2]*255, 50))
        display.blit(current_height_marker, (display.get_width()/2 - current_height_marker.get_width()/2, cam_offset + round(
            (player.position.y - starting_height)/display.get_height())*display.get_height() + player.current_sprite.get_height() - 40))

        for bean in beans:
            display.blit(bean.sprite, (bean.position.x,
                         bean.position.y + cam_offset))

        display.blit(pygame.transform.rotate(player.current_sprite, clamp(
            player.velocity.y, -10, 5)*player.rot_offset), (player.position.x, player.position.y + cam_offset))
        display.blit(shop_bg.sprite, (0, 0))
        pygame.draw.rect(display, (81, 48, 20),
                         (21, 437, 150*(player.health/100), 25))
        display.blit(shop.sprite, (0, 0))

        for button in buttons:
            display.blit(button.sprite, (220 + (button.index*125), 393))
            price_display = font_small.render(
                str(button.price), True, (0, 0, 0))
            display.blit(price_display, (262 + (button.index*125), 408))
            level_display = font_20.render(
                f'Lvl. {button.level}', True, (200, 200, 200))
            display.blit(level_display, (234 + (button.index*125), 441))
            display.blit(button.type_indicator_sprite,
                         (202 + (button.index*125), 377))

        bean_count_display = font_small.render(
            str(player.bean_count).zfill(7), True, (0, 0, 0))
        display.blit(bean_count_display, (72, 394))

        if player.dead:
            display.blit(retry_button.sprite, (4, 4))
            death_message = font_small.render("RETRY", True, (0, 0, 0))
            display.blit(death_message, (24, 8))

        if (scroll):
            player.set_height(
                round(-(player.position.y - starting_height)/display.get_height()))
            player.position.x += player.velocity.x*dt
            if player.position.x - 5 < 0 or player.position.x + player.current_sprite.get_size()[0] + 5 > display.get_width():
                player.flip()
            if jump and not player.dead:
                player.velocity.y = -player.flap_force
                Sound.play(flapfx)
            player.position.y += player.velocity.y*dt
            player.velocity.y = clamp(
                player.velocity.y + player.acceleration*dt, -99999999999, 50)

        if not player.dead:
            player.health -= 0.2*dt
            if player.health <= 0:
                player.kill(deadfx)

        for bean in beans:
            if bean.position.y + cam_offset + 90 > display.get_height():
                bean.position.y -= display.get_height()*2
                bean.position.x = random.randrange(
                    0, display.get_width() - bean.sprite.get_width())
            if (check_collisions(player.position.x, player.position.y, player.current_sprite.get_width(), player.current_sprite.get_height(), bean.position.x, bean.position.y, bean.sprite.get_width(), bean.sprite.get_height())):
                Sound.play(beanfx)
                player.bean_count += 1
                player.health = 100
                bean.position.y -= display.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(
                    0, display.get_width() - bean.sprite.get_width())

        for button in buttons:
            if clicked and not player.dead and check_collisions(mouse_x, mouse_y, 3, 3, button.position.x, button.position.y, button.sprite.get_width(), button.sprite.get_height()):
                if (player.bean_count >= button.price):
                    Sound.play(upgradefx)
                    button.level += 1
                    player.bean_count -= button.price
                    button.price = round(button.price*2.5)
                    if (button.index == 0):
                        player.flap_force *= 1.5
                    if (button.index == 1):
                        player.velocity.x *= 1.5
                    if (button.index == 2):
                        bean_multiplier += 5
                        for _ in range(bean_multiplier):
                            beans.append(Bean(random.randrange(0, display.get_width() - Bean().sprite.get_width(
                            )), player.position.y - display.get_height() - random.randrange(0, 200)))

        if player.dead and clicked and check_collisions(mouse_x, mouse_y, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            start()

        bg[0].position = cam_offset + \
            round(player.position.y/display.get_height())*display.get_height()
        bg[1].position = bg[0].position + display.get_height()
        bg[2].position = bg[0].position - display.get_height()

        Display.update()
        await asyncio.sleep(0)
        pygame.time.delay(10)

if __name__ == "__main__":
    asyncio.run(main())
