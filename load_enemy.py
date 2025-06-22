import pygame
import os
import constant as const

def change_scale(image:pygame.Surface, factor):
        scaled_img = pygame.transform.scale(image, (image.get_width() * factor, image.get_height() * factor))
        return scaled_img

def load_bat():
    animation = {
            "fly" : [],
            "hang" : [],
        }
    
    for fly in range(3):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"bat/bat-fly/bat-fly{fly + 1}.png")), const.PLAYER_FACTOR)
        animation["fly"].append(image)
    
    return animation