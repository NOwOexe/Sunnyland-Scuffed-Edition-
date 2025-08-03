import pygame
import os
import json
import constant as const

class World():
    
    def __init__(self, screen):
        self.data = {}
        with open(os.path.join(const.MAP_PATH, "map.json"), "r") as file:
            self.data = json.load(file)
            
        self.map = self.load_map()
        self.map_layer, self.collidable = self.load_layer()
        self.map_layer.reverse()
        self.collidable.reverse()
        
        self.screen = screen
        
    def change_scale(self, image:pygame.Surface, factor):
        scaled_img = pygame.transform.scale(image, (image.get_width() * factor, image.get_height() * factor))
        return scaled_img

    def load_map(self):
        tile_map = {}
        
        original_image = pygame.image.load(os.path.join(const.MAP_PATH, "spritesheet.png")).convert_alpha()
        original_image = self.change_scale(original_image, const.MAP_FACTOR)
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
        map_factor = const.MAP_FACTOR
        for layers in self.data["layers"]:
            map_layer.append(layers)
            if layers["collider"]:
                for tile in layers["tiles"]:
                    tile_x, tile_y, tile_size = tile["x"], tile["y"], self.data["tileSize"]
                    tile_rect = pygame.Rect(tile_x * tile_size * map_factor, tile_y * tile_size * map_factor,
                                            tile_size * map_factor, tile_size * map_factor)
                    collidable.append(tile_rect)
        return (map_layer, collidable)
    
    def draw_map(self):
        for layer in self.map_layer:
            for tiles in layer["tiles"]:
                self.screen.blit(self.map[int(tiles["id"])], (tiles["x"] * const.TILE_SIZE, tiles["y"] * const.TILE_SIZE))
    
    def draw_collide(self):
        for tiles in self.collidable:
            pygame.draw.rect(self.screen, const.G_COLOR, tiles, 1)