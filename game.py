import pygame, os, time
from player import Player
from levels.map import Map

from OpenGL.GL import *
from OpenGL.GLU import *

class Game():
    def __init__(self):
        pygame.init()
        self.DISPLAY_W, self.DISPLAY_H = 1024, 510
        self.DISPLAY3D_W, self.DISPLAY3D_H = 320, 160
        self.display_open_gl(self.DISPLAY_W,self.DISPLAY_H)
        self.running, self.playing = True, True
        self.dir = os.path.dirname(os.path.abspath("game.py"))
        self.actions = {"left": False, "right": False, "up" : False, "down" : False}
        self.TARGET_FPS = 60
        self.prev_time = time.time()
        self.player = Player(self)
        self.map = Map(self)
        self.fps_list = []

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()


    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                

    def update(self):
        self.player.update()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.map.draw()
        self.player.draw()
        self.player.drawRays()
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
        self.get_fps()

    def reset_keys(self):
        for key in self.actions:
            self.actions[key] = False

    def display_open_gl(self,w,h):
        pygame.display.set_mode((w,h), pygame.OPENGL|pygame.DOUBLEBUF)
        glClearColor(0,0,0,0)
        gluOrtho2D(0,1024,512,0)

    def get_fps(self):
        fps = 0
        if self.dt: fps = 1/self.dt
        if len(self.fps_list) == 50:
            self.fps_list.pop(0)
        self.fps_list.append(fps)
        avg_fps = sum(self.fps_list) / len(self.fps_list)
        pygame.display.set_caption('Raycaster - FPS:' + str(round(avg_fps,2)))
        
        

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()