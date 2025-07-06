import pygame
import constant as const
from player import *
        
class Enemy():
    def __init__(self, animation, x, y, state):
        self.image = animation[state][0]
        self.animation = animation
        self.rect = self.image.get_rect(x = x, y = y)
        self.start_time = pygame.time.get_ticks()
        self.state = state
        self.flippped = False
        self.frame = 0
        
    def draw(self, screen:pygame.Surface):
        flipped_image = pygame.transform.flip(self.image, self.flippped, False)
        screen.blit(flipped_image, (self.rect.x, self.rect.y))
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
        self.aggro_rect = pygame.Rect(x - (const.AGGRO_W - self.rect.w) / 2, y - const.AGGRO_H / 2 + 16, const.AGGRO_W, const.AGGRO_H)
        self.start_time = pygame.time.get_ticks()
        self.x_pos = float(self.rect.x)
        self.aggro_pos = float(self.aggro_rect.x)
        
    def draw(self, screen:pygame.Surface):
        flipped_image = pygame.transform.flip(self.image, self.flippped, False)
        screen.blit(flipped_image, (self.rect.x - self.offset_x, self.rect.y - self.offset_y))
        pygame.draw.rect(screen, const.G_COLOR, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 1)
        pygame.draw.rect(screen, const.B_COLOR, self.aggro_rect, 1)
        
    def move(self, player:Player, delta_time):
        if player.rect.colliderect(self.aggro_rect):
            if player.rect.x >= self.rect.x:
                self.state = "run"
                self.flippped = True
                self.x_pos += const.SLIME_SPEED * delta_time
                self.aggro_pos += const.SLIME_SPEED * delta_time
                self.rect.x = int(self.x_pos)
                self.aggro_rect.x = int(self.aggro_pos)
            if player.rect.x <= self.rect.x:
                self.state = "run"
                self.flippped = False
                self.x_pos -= const.SLIME_SPEED * delta_time
                self.aggro_pos -= const.SLIME_SPEED * delta_time
                self.rect.x = int(self.x_pos)
                self.aggro_rect.x = int(self.aggro_pos)
        else:
            self.state = "idle"
            
class Bat(Enemy):
    def __init__(self, animation, x, y, state):
        super().__init__(animation, x, y, state)
        self.min_height = self.rect.y + 100
        self.max_height = self.rect.y - 100
        self.y_pos = float(self.rect.y)
        self.direction = 1
        
    def move(self, delta_time):
        if self.rect.y >= self.min_height:
            self.direction *= -1
        if self.rect.y <= self.max_height:
            self.direction *= -1
        self.y_pos += const.BAT_FLY_SPEED * delta_time * self.direction
        self.rect.y = int(self.y_pos)
        
class Frog(Enemy):
    def __init__(self, animation, x, y, state):
        super().__init__(animation, x, y, state)
        self.min_dx = self.rect.x - 100
        self.max_dx = self.rect.x + 100
        self.velocity_y = 0
        self.x_pos = float(self.rect.x)
        self.direction = 1
        self.state = "idle"
        
    def move(self, delta_time):
        if self.rect.x >= self.max_dx:
            self.state = "jump"
            self.direction *= -1
        if self.rect.x <= self.min_dx:
            self.state = "jump"
            self.direction *= -1
        if self.state != "jump":
            self.velocity_y = const.FROG_JUMPFORCE
            
        self.rect.y += self.velocity_y * delta_time
        self.velocity_y += const.GRAVITY
        self.x_pos += const.FROG_SPEED * delta_time * self.direction
        self.rect.x = int(self.x_pos)