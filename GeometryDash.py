# -*- coding: utf-8 -*-

import pygame
from random import randint

pygame.init()

score = 0
total = 0

myfont = pygame.font.SysFont('monospace', 50)

Vel = 0
Jumping = 0
Dead = False

display = {
  'width': 800,
  'height': 600
}

character = {
  'width': 20,
  'height': 20,
  'x': 200,
  'y': 580,
  'velocity': 50
}


platform = {
    'y': 580,
    'x': 700,
    'pass': 0,
    'length': 20,
    'ammount': 2,
    'distanceApart': 50
}
spike = {
  'height': -15,
  'y': 600,
  'x': 700,
  'pass': 0,
  'length': 20,
  'ammount': 2,
  'distanceApart': 50
}


def nextSection(a):
    spike['x'] = 1000
    spike['pass'] = spike['pass'] + spike['ammount']
    spike['ammount'] = randint(1, 5)
    spike['distanceApart'] = randint(2, 8) * 10
    return a + 1


def triangleDraw(i):
    pygame.draw.polygon(win, (0, 0, 0), ((spike['x'] + spike['distanceApart'] * i, spike['y']),
                                     (spike['x'] + spike['distanceApart'] * i + spike['length'], spike['y']),
        (spike['x'] + spike['length'] / 2 + spike['distanceApart'] * i, spike['y'] + spike['height'])))


def jump():
    global Vel
    global Jumping
    if Jumping == 0:
        Jumping = 1
        Vel = 10
        character['y'] = character['y'] - Vel
        if character['y'] > platform['y']:
            Jumping = 0
        Vel = Vel - 0.5


def ContinueJump():
    global Vel
    global Jumping
    if Jumping == 0:
        if character['y'] > platform['y']:
            pass
        else:
            Jumping = 1
    if Jumping == 1:
        character['y'] = character['y'] - Vel
        if character['y'] > platform['y']:
            Jumping = 2
        Vel = Vel - 0.5
    elif Jumping == 2:
        Jumping = 3
    elif Jumping == 3:
        Jumping = 4
    elif Jumping == 4:
        Jumping = 5
    elif Jumping == 5:
        Jumping = 0


def next():
    ContinueJump()
    pygame.draw.rect(win, (255, 204, 0), (character['x'], character['y'], character['width'], character['height']))
    pygame.display.update()
    spike['x'] = spike['x'] - 5

win = pygame.display.set_mode((display['width'], display['height']))

jump()
while True:
    pygame.time.delay(10)
    win.fill((255, 255, 255))
    for i in range(spike['ammount']):
        triangleDraw(i)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
            jump()
    if spike['x'] + spike['distanceApart'] * spike['ammount'] < character['x']:
        i = nextSection(i)
    if spike['pass'] < 100:
        textsurface2 = myfont.render('Пройдено {0}%'.format(spike['pass']), False, (0, 0, 0))
        win.blit(textsurface2, (300, 10))
    else:
        textsurface2 = myfont.render('ВЫ ПОБЕДИЛИ', False, (255, 0, 0))
        win.blit(textsurface2, (300, 50))
        break
    for i in range(spike['ammount']):
        if (spike['x'] + spike['distanceApart'] * i <= character['x']) and (spike['x'] + spike['distanceApart'] *
        i + spike['length'] >= character['x']):
            posOfSpike = abs(character['x'] - (spike['x'] + spike['length'] / 2))
            if (posOfSpike * 2 + spike['y'] > character['y']) and (spike['y'] < character['y']
            or posOfSpike * 2 + spike['y'] > character['y'] + character['height']) and (spike['y'] < character['y'] + character['height']):
                textsurface2 = myfont.render('ВЫ ПРОИГРАЛИ', False, (255, 0, 0))
                win.blit(textsurface2, (300, 50))
                Dead = True
        else:
            None
    next()
    if Dead:
        break
pygame.time.delay(1000)
