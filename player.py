import pygame

class Player():
    def __init__(self, animation, x, y):
        self.image = animation["idle"][0]
        self.animation = animation
        self.rect = self.image.get_rect(x = x, y = y)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self):
        pass