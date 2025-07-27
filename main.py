import pygame
import os
import json
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
        self.bat = Bat(bat_animation, 100, 300, "fly")
        
        frog_animation = load_frog()
        self.frog = Frog(frog_animation, 100, const.SCREEN_H - frog_animation["idle"][0].get_height(), "idle")
        
        slime_animation = load_slime()
        slime_offset = const.SLIME_OFFSET_H
        self.slime = Slime(slime_animation, 200, const.SCREEN_H - slime_animation["idle"][0].get_height() + slime_offset, "idle")
        
        self.start_time = pygame.time.get_ticks()
        
        self.data = {}
        #Map
        with open(os.path.join(const.MAP_PATH, "map.json"), "r") as file:
            self.data = json.load(file)
            
        self.map = self.load_map()
        self.map_layer, self.collidable = self.load_layer()
        self.map_layer.reverse()

    def load_map(self):
        tile_map = {}
        
        original_image = pygame.image.load(os.path.join(const.MAP_PATH, "spritesheet.png")).convert_alpha()
        original_image = change_scale(original_image, const.MAP_FACTOR)
        img_w, img_h = original_image.get_size()
        tile_size = self.data["tileSize"] * const.MAP_FACTOR
        tile_id = 0
        for col in range(0, img_h, tile_size):
            for row in range(0, img_w, tile_size):
                sub_img = original_image.subsurface(row, col, tile_size, tile_size)
                tile_map[tile_id] = sub_img
                tile_id += 1
        return tile_map
    
    def load_layer(self):
        map_layer = []
        collidable = []
        for layers in self.data["layers"]:
            map_layer.append(layers)
            if layers["collider"]:
                for tile in layers["tiles"]:
                    tile_x, tile_y, tile_size = tile["x"], tile["y"], self.data["tileSize"]
                    tile_rect = pygame.Rect(tile_x * tile_size, tile_y * tile_size,
                                            tile_size, tile_size)
                    collidable.append(tile_rect)
        return (map_layer, collidable)
    
    def draw_map(self):
        for layer in self.map_layer:
            for tiles in layer["tiles"]:
                self.screen.blit(self.map[int(tiles["id"])], (tiles["x"] * const.TILE_SIZE, tiles["y"] * const.TILE_SIZE))
        
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
            delta_time = (cur_time - self.start_time) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.screen.fill((0, 0, 0))
            self.draw_map()
            self.player.draw(self.screen)
            self.player.update()
            self.player.move()
            self.bat.draw(self.screen)
            self.bat.update()
            self.bat.move(delta_time)
            self.frog.draw(self.screen)
            self.frog.update()
            self.frog.move(delta_time)
            self.slime.draw(self.screen)
            self.slime.update()
            self.slime.move(self.player, delta_time)
            self.start_time = cur_time
            pygame.display.update()
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()