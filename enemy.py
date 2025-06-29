import pygame
import constant as const
        
class Enemy():
    def __init__(self, animation, x, y, state):
        self.image = animation[state][0]
        self.animation = animation
        self.rect = self.image.get_rect(x = x, y = y)
        self.start_time = pygame.time.get_ticks()
        self.state = state
        self.frame = 0
        
    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, const.G_COLOR, self.rect, 1)
        
    def update(self):
        cur_time = pygame.time.get_ticks()
        delta_time = (cur_time - self.start_time) / 1000
        if delta_time > const.ANIMATION_COOLDOWN:
            if self.frame < len(self.animation[self.state]):
                self.image = self.animation[self.state][self.frame]
                self.frame += 1
            else:
                self.frame = 0
            self.start_time = cur_time
            
class Slime(Enemy):
    def __init__(self, animation, x, y, state):
        super().__init__(animation, x, y, state)
        self.offset_x = const.SLIME_OFFSET_X
        self.offset_y = const.SLIME_OFFSET_Y
        self.offset_w = const.SLIME_OFFSET_W
        self.offset_h = const.SLIME_OFFSET_H
        self.rect.w -= self.offset_w
        self.rect.h -= self.offset_h
        self.aggro_rect = pygame.Rect(x - (const.AGGRO_W - self.rect.w) / 2, y - const.AGGRO_H / 2, const.AGGRO_W, const.AGGRO_H)
        
    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, (self.rect.x - self.offset_x, self.rect.y - self.offset_y))
        pygame.draw.rect(screen, const.G_COLOR, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 1)
        pygame.draw.rect(screen, const.B_COLOR, self.aggro_rect, 1)
        
    def move(self):
        pass