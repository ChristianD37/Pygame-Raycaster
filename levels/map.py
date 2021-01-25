import pygame, os,csv

from OpenGL.GL import *
from OpenGL.GLU import *

class Map():
    def __init__(self, game):
        self.game = game
        self.grid_x, self.grid_y = 8,8
        self.grid_size = 64
        self.load_world()

    def draw(self):
        y = 0
        for layer in self.map_grid:
            x = 0
            for tile in layer:
                x_off, y_off = x * self.grid_size, y * self.grid_size
                # Empty space, do nothing
                if tile == 1: glColor3f(1,1,1)
                else: glColor3f(0,0,0)
                glBegin(GL_QUADS)
                glVertex2i(x_off + 1,y_off + 1)
                glVertex2i(x_off + 1,y_off + self.grid_size - 1)
                glVertex2i(x_off + self.grid_size - 1, y_off + self.grid_size - 1)
                glVertex2i(x_off + self.grid_size - 1, y_off + 1)
                glEnd()
                x +=1
            y+=1

    def load_world(self):
        # Loads the world from a csv file
        with open(os.path.join(self.game.dir, "levels","level.csv")) as data:
            data = csv.reader(data,delimiter = ',')
            self.map_grid = []
            for row in data:
                self.map_grid.append(list(row))
            # Covert the indices from strings to ints
            for row in self.map_grid:
                for index in range(len(row)):
                    row[index] = int(row[index])
            

        