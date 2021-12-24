import pygame as pg
import numpy as np
import math

height_map_img = pg.image.load('img/heightmap.png')
height_map = pg.surfarray.array3d(height_map_img)

class Player:
    def __init__(self):
        self.pos = np.array([0, 0], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 40
        self.angle_vel = 0.01
        self.vel = 8
        self.vertical_angle = 0
        
        

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_UP]:
            if(self.vertical_angle<  math.pi / 2):
                self.pitch += self.vel
                self.vertical_angle += self.angle_vel
                

        if pressed_key[pg.K_DOWN]:
            if(self.vertical_angle> - math.pi / 2):
                self.pitch -= self.vel
                self.vertical_angle -= self.angle_vel
                

        if pressed_key[pg.K_LEFT]:
            self.angle -= self.angle_vel
        if pressed_key[pg.K_RIGHT]:
            self.angle += self.angle_vel

        if pressed_key[pg.K_w]:
            
            if (10 < int(self.pos[0] + self.vel * cos_a * math.cos(self.vertical_angle)) + 20 < len(height_map) and 10 < int(self.pos[1] + self.vel * sin_a) + 20< len(height_map[0]) and self.height + self.vel * math.sin(self.vertical_angle) > height_map[int(self.pos[0] + self.vel * cos_a * math.cos(self.vertical_angle)) , int(self.pos[1] + self.vel * sin_a)  ][0] + 20 and 
                self.height + self.vel * math.sin(self.vertical_angle)< 350):
                self.height += self.vel * math.sin(self.vertical_angle)
                self.pos[0] += self.vel * cos_a * math.cos(self.vertical_angle)
                self.pos[1] += self.vel * sin_a 
            

        if pressed_key[pg.K_s]:
            
            if (10 < int(self.pos[0] - self.vel * cos_a * math.cos(self.vertical_angle)) + 20 < len(height_map) and  10 < int(self.pos[1] - self.vel * sin_a) + 20 < len(height_map[0]) and self.height + self.vel * math.sin(self.vertical_angle) > height_map[int(self.pos[0] - self.vel * cos_a * math.cos(self.vertical_angle)) , int(self.pos[1] - self.vel * sin_a)][0] + 20 and self.height - self.vel * math.sin(self.vertical_angle)< 350):
                self.height -= self.vel * math.sin(self.vertical_angle)
                self.pos[0] -= self.vel * cos_a * math.cos(self.vertical_angle)
                self.pos[1] -= self.vel * sin_a 

            

        if pressed_key[pg.K_a]:
            if (10 < int(self.pos[0] + self.vel * sin_a) + 20< len(height_map) and  10 < int(self.pos[1] - self.vel * cos_a) + 20 < len(height_map[0]) and self.height + self.vel * math.sin(self.vertical_angle) > height_map[int(self.pos[0] + self.vel * sin_a) , int(self.pos[1] - self.vel * cos_a)][0] + 20 and self.height + self.vel * math.sin(self.vertical_angle)< 350):
                self.pos[0] += self.vel * sin_a
                self.pos[1] -= self.vel * cos_a

        if pressed_key[pg.K_d]:
            if (10 < int(self.pos[0] - self.vel * sin_a) + 20 < len(height_map) and  10 < int(self.pos[1] + self.vel * cos_a) + 20 < len(height_map[0])and self.height + self.vel * math.sin(self.vertical_angle) > height_map[int(self.pos[0] - self.vel * sin_a) , int(self.pos[1] + self.vel * cos_a)][0] + 20 and self.height + self.vel * math.sin(self.vertical_angle)< 350):
                
                self.pos[0] -= self.vel * sin_a
                self.pos[1] += self.vel * cos_a
