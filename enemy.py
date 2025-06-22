import pygame

class Enemy():
    def __init__(self, animation, x, y):
        self.image = animation["fly"][0]
        self.animation = animation
        self.rect = self.image.get_rect(x = x, y = y)
        
    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))