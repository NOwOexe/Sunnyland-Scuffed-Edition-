import pygame
import os
import constant as const
from player import *
from enemy import *
from load_enemy import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sunnyland (Scuffed Edition)")
        self.screen = pygame.display.set_mode((const.SCREEN_W, const.SCREEN_H))
        
        #Player
        player_animation = self.load_player_animation()
        self.player = Player(player_animation, const.SCREEN_W // 2, const.SCREEN_H - player_animation["idle"][0].get_height() + const.PLAYER_OFFSET_H)
        
        #Enemy
        bat_animation = load_bat()
        self.bat = Enemy(bat_animation, 0, 0, "fly")
        
        frog_animation = load_frog()
        self.frog = Enemy(frog_animation, 100, 0, "idle")
        
        slime_animation = load_slime()
        slime_offset = const.SLIME_OFFSET_H
        self.slime = Slime(slime_animation, 200, const.SCREEN_H - slime_animation["idle"][0].get_height() + slime_offset, "idle")
        
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            self.player.update()
            self.player.move()
            self.bat.draw(self.screen)
            self.bat.update()
            self.frog.draw(self.screen)
            self.frog.update()
            self.slime.draw(self.screen)
            self.slime.update()
            self.slime.move()
            pygame.display.update()
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()