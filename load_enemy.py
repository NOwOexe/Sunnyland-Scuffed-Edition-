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
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"bat/bat-fly/bat-fly{fly + 1}.png")), const.BAT_FACTOR)
        animation["fly"].append(image)
        
    for hang in range(4):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"bat/bat-hang/bat-hang{hang + 1}.png")), const.BAT_FACTOR)
        animation["hang"].append(image)
    
    return animation

def load_frog():
    animation = {
            "idle" : [],
            "jump" : [],
        }
    
    for idle in range(4):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"frog/Sprites/idle/frog-idle-{idle + 1}.png")), const.FROG_FACTOR)
        animation["idle"].append(image)
        
    for jump in range(2):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"frog/Sprites/jump/frog-jump-{jump + 1}.png")), const.FROG_FACTOR)
        animation["jump"].append(image)
    
    return animation

def load_slime():
    animation = {
            "idle" : [],
            "run" : [],
        }
    
    for idle in range(8):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"Slimer/Sprites/Slimer-Idle/slimer-idle{idle + 1}.png")), const.SLIME_FACTOR)
        animation["idle"].append(image)
        
    for run in range(7):
        image = change_scale(pygame.image.load(os.path.join(const.ENEMY_PATH, f"Slimer/Sprites/Slimer-Run/slimer{run + 1}.png")), const.SLIME_FACTOR)
        animation["run"].append(image)
    
    return animation