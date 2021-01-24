import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

class Player():
    def __init__(self, game):
        self.game = game
        self.position = pygame.Vector2(300,300)
        self.rect = pygame.Rect(300,300,8,8)
        self.speed = 150

    def update(self):
        if self.game.actions["left"]: self.position.x -= self.speed * self.game.dt
        if self.game.actions["right"]: self.position.x += self.speed * self.game.dt
        if self.game.actions["up"]: self.position.y -= self.speed * self.game.dt
        if self.game.actions["down"]: self.position.y += self.speed * self.game.dt

    def draw(self):
        glColor3f(1,1,0)
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex2i(int(self.position.x), int(self.position.y))
        glEnd()