import pygame, math

from OpenGL.GL import *
from OpenGL.GLU import *


class Player():
    def __init__(self, game):
        self.game = game
        self.position = pygame.Vector2(300,300)
        self.rect = pygame.Rect(300,300,8,8)
        self.speed = 150
        self.player_angle = 1
        self.position_delta = pygame.Vector2(math.cos(self.player_angle) * 5,math.sin(self.player_angle)*5)
        self.ONE_DEGREE = .0174533
        self.final_distance = 1

    def update(self):
        # Handles moving the player's coordinates in the 2D space
        if self.game.actions["left"]: 
            self.player_angle -= 6 * self.game.dt
            if self.player_angle < 0: self.player_angle += 2 * math.pi
            self.rotate_player()
        if self.game.actions["right"]:
            self.player_angle += 6 * self.game.dt
            if self.player_angle > 2 * math.pi: self.player_angle -= 2 * math.pi
            self.rotate_player()
        if self.game.actions["up"]: self.move_player(1)
        if self.game.actions["down"]: self.move_player(-1)

    def is_colliding(self, x, y):
        rel_x = int(x) >> 6
        rel_y = int(y) >> 6
        return self.game.map.map_grid[rel_y][rel_x]

    def rotate_player(self):
        self.position_delta.x = math.cos(self.player_angle) * 5 
        self.position_delta.y = math.sin(self.player_angle) * 5 

    def move_player(self, direction):
        # Calculate new position
        newx = self.position.x +self.position_delta.x *   self.game.dt * direction * 10
        newy = self.position.y + self.position_delta.y *   self.game.dt * direction * 10
        # Check if new position is a wall. If it is, don't move
        if not self.is_colliding(newx,newy):
            self.position.x = newx
            self.position.y = newy

    # Draws the player in the 2D space
    def draw(self):
        int_x, int_y = int(self.position.x), int(self.position.y)
        glColor3f(1,1,0)
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex2i(int_x, int_y)
        glEnd()

        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex2i(int_x, int_y)
        glVertex2i(int_x + int(self.position_delta.x) * 5, int_y + int(self.position_delta.y) * 5)
        glEnd()

    # Draws the rays in the 2D space and walls in 3D space
    def drawRays(self):
        int_x, int_y = int(self.position.x), int(self.position.y)
        self.ray_angle = self.radian_bound(self.player_angle - 30 * self.ONE_DEGREE)
        for i in range(0,60):
            # Draw 2D rays
            self.Check_Horizontal_Lines()
            self.Check_Vertical_Lines()
            # Check for which ray is shorter
            ray_x, ray_y, self.final_distance = self.hray_x, self.hray_y, self.Hdist
            glColor3f(1,1,1) 
            if self.Vdist < self.Hdist:
                ray_x, ray_y = self.vray_x, self.vray_y
                self.final_distance = self.Vdist
                glColor3f(.9,.9,.9) 
            glLineWidth(1) 
            glBegin(GL_LINES)
            glVertex2i(int_x,int_y)
            glVertex2i(int(ray_x),int(ray_y))
            glEnd()
            # Draw 3D Walls
            # Draw the 3D walls
            cos_angle = self.radian_bound(self.player_angle - self.ray_angle) # Fix Fish eye effect
            self.final_distance *= math.cos(cos_angle)
            line_height = min((self.game.map.grid_size*self.game.DISPLAY3D_W)/self.final_distance,self.game.DISPLAY3D_W)
            offset3d = int(self.game.DISPLAY3D_H - line_height/2)
            glLineWidth(8)
            glBegin(GL_LINES)
            glVertex2i(i*8 + 530,offset3d)
            glVertex2i(i*8 + 530,int(line_height) + offset3d)
            glEnd()
            # Increment angle by one degree
            self.ray_angle = self.radian_bound( self.ray_angle + self.ONE_DEGREE)

    
    def Check_Horizontal_Lines(self):
        self.Hdist, self.hray_x, self.hray_y = 10000,0,0
        int_x, int_y = int(self.position.x), int(self.position.y)
        ray_x,ray_y,dof,y_off,x_off = 0,0,0,0,0
        aTan = -1 / math.tan(self.ray_angle)
        if self.ray_angle > math.pi: # Check for Grid Lines looking Up
            ray_y = ((int_y >>6)<<6) - .0001
            ray_x = (self.position.y - ray_y) * aTan + self.position.x
            y_off = -64
            x_off = -y_off * aTan
        elif self.ray_angle < math.pi: # Check for grid lines looking down
            ray_y = ((int_y >>6)<<6) + 64
            ray_x = (self.position.y - ray_y) * aTan + self.position.x
            y_off = 64
            x_off = -y_off * aTan
        else:
            ray_x, ray_y = self.player.x, self.player.y
            dof = 8
        
        while dof < 8:
            map_x = int(ray_x) >> 6
            map_y = int(ray_y) >> 6
            map_x = max(min(map_x,self.game.map.grid_x - 1),0)
            map_y = max(min(map_y,self.game.map.grid_y - 1),0)
            if self.game.map.map_grid[map_y][map_x] == 1: # Wall has been hit, return ray info
                self.hray_x, self.hray_y = ray_x, ray_y
                self.Hdist = math.hypot(self.position.x - self.hray_x, self.position.y - self.hray_y)
                dof = 8
            else: # Continue up or down the grid by using the offset
                ray_x += x_off
                ray_y += y_off
                dof += 1


    def Check_Vertical_Lines(self):
        self.Vdist, self.vray_x, self.vray_y = 10000,0,0
        HALF_PI = math.pi/2
        THREE_PI_DIV2 = 3*math.pi/2
        int_x, int_y = int(self.position.x), int(self.position.y)
        ray_x,ray_y,dof,y_off,x_off = 0,0,0,0,0
        nTan = -1*math.tan(self.ray_angle)
        if self.ray_angle > HALF_PI and self.ray_angle < THREE_PI_DIV2: # Check for grid lines facing left
            ray_x = ((int_x >>6)<<6) - .0001
            ray_y = (self.position.x - ray_x) * nTan + self.position.y
            x_off = -64
            y_off = -x_off * nTan
        elif self.ray_angle < HALF_PI or self.ray_angle > THREE_PI_DIV2:# Check for grid lines facing right
            ray_x = ((int_x >>6)<<6) + 64
            ray_y = (self.position.x - ray_x) * nTan + self.position.y
            x_off = 64
            y_off = -x_off * nTan
        else:
            ray_x, ray_y = self.player.x, self.player.y
            dof = 8
        
        while dof < 8:
            map_x = int(ray_x) >> 6
            map_y = int(ray_y) >> 6
            map_x = max(min(map_x,7),0)
            map_y = max(min(map_y,7),0)
            if self.game.map.map_grid[map_y][map_x] == 1: 
                self.vray_x, self.vray_y = ray_x, ray_y
                self.Vdist = math.hypot(self.position.x - self.vray_x, self.position.y - self.vray_y)
                dof = 8
            else:
                ray_x += x_off
                ray_y += y_off
                dof += 1

    # Helper function to keep radian values in between 0 and 2pi
    def radian_bound(self, value):
        if value > 2 * math.pi: value -= 2 * math.pi
        if value < 0: value += 2 * math.pi
        return value