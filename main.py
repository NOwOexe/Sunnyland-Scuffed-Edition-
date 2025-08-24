import pygame
import os
import json
import constant as const
from player import *
from enemy import *
from load_enemy import *
from world import *
from camera import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sunnyland (Scuffed Edition)")
        self.screen = pygame.display.set_mode((const.SCREEN_W, const.SCREEN_H))
        #Player
        player_animation = self.load_player_animation()
        self.player = Player(player_animation, const.SCREEN_W // 2, 0)
        #Enemy
        bat_animation = load_bat()
        frog_animation = load_frog()
        slime_animation = load_slime()
        self.bat = Bat(bat_animation, 100, 300, "fly")
        self.frog = Frog(frog_animation, 100, const.SCREEN_H - frog_animation["idle"][0].get_height(), "idle")
        slime_offset = const.SLIME_OFFSET_H
        self.slime = Slime(slime_animation, 200, const.SCREEN_H - slime_animation["idle"][0].get_height() + slime_offset, "idle")
        self.start_time = pygame.time.get_ticks()
        
        #World
        self.world = World(self.screen)
        
        #Camera
        world_w,world_h = self.world.get_world_size()
        self.camera = Camera((const.SCREEN_W, const.SCREEN_H), (world_w, world_h), deadzone=(300, 180))
        
    def change_scale(self, image:pygame.Surface, factor):
        scaled_img = pygame.transform.scale(image, (image.get_width() * factor, image.get_height() * factor))
        return scaled_img
        
    def load_player_animation(self):
        animation = {
            "idle" : [],
            "run" : [],
            "jump" : []
        }
        
        for idle in range(4):
            image = self.change_scale(pygame.image.load(os.path.join(const.PLAYER_PATH, f"idle/Sprites/idle-{idle + 1}.png")), const.PLAYER_FACTOR)
            animation["idle"].append(image)
            
        for run in range(8):
            image = self.change_scale(pygame.image.load(os.path.join(const.PLAYER_PATH, f"run/Sprites/run-{run + 1}.png")), const.PLAYER_FACTOR)
            animation["run"].append(image)
            
        for jump in range(5):
            image = self.change_scale(pygame.image.load(os.path.join(const.PLAYER_PATH, f"jump/Sprites/jump-{jump + 1}.png")), const.PLAYER_FACTOR)
            animation["jump"].append(image)
            
        return animation
    
    def run(self):
        run = True
        while run:
            cur_time = pygame.time.get_ticks()
            delta_time = (cur_time - self.start_time) / 1000.0
            self.start_time = cur_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.camera.update(self.player.rect)
            self.screen.fill((0, 0, 0))
            self.world.draw_map(self.camera)
            
            self.world.draw_collide(self.camera) #debug :))))
            
            self.player.move()
            self.player.check_collide(self.world.collidable)
            self.player.update()
            self.player.draw(self.screen, self.camera)
            
            self.bat.draw(self.screen, self.camera)
            self.bat.update()
            self.bat.move(delta_time)
            
            self.frog.draw(self.screen, self.camera)
            self.frog.update()
            self.frog.move(self.world.collidable, delta_time)
            
            self.slime.draw(self.screen, self.camera)
            self.slime.update()
            self.slime.move(self.player, delta_time)
            self.slime.check_collide(self.world.collidable)
            self.slime.gravity(self.world.collidable)
            pygame.display.update()
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()