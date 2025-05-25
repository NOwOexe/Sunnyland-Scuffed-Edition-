import pygame
import os
import constant as const
from player import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sunnyland (Scuffed Edition)")
        self.screen = pygame.display.set_mode((const.SCREEN_W, const.SCREEN_H))
        
        #Player
        player_animation = self.load_player_animation()
        self.player = Player(player_animation, const.SCREEN_W // 2, const.SCREEN_H // 2)
        
    def load_player_animation(self):
        animation = {
            "idle" : [],
            "walk" : [],
            "run" : []
        }
        for idle in range(4):
            image = pygame.image.load(os.path.join(const.PLAYER_PATH, f"idle/Sprites/idle-{idle + 1}.png"))
            animation["idle"].append(image)
            
        return animation
    
    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.player.draw(self.screen)
            pygame.display.update()
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()