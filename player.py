import pygame
import constant as const

class Player():
    def __init__(self, animation, x, y):
        self.image = animation["idle"][0]
        self.animation = animation
        self.rect = self.image.get_rect(x = x, y = y)
        self.rect.w -= const.PLAYER_OFFSET_W
        self.rect.h -= const.PLAYER_OFFSET_H
        self.frame = 0
        self.update_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.speed = const.PLAYER_SPEED
        self.x_pos = float(x)
        self.is_flipped = False
        self.is_moving = False
        self.state = "idle"
        self.stop_frame = False
    
    def draw(self, screen):
        flipped_img = pygame.transform.flip(self.image, self.is_flipped, False)
        screen.blit(flipped_img, (self.rect.x - const.PLAYER_OFFSET_X, self.rect.y - const.PLAYER_OFFSET_Y))
        pygame.draw.rect(screen, const.G_COLOR, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 1)
        
    def move(self):
        dx = 0
        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.start_time) / 1000
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.is_flipped = True
            dx = -1
        if key[pygame.K_d]:
            self.is_flipped = False
            dx = 1
        if dx != 0:
            self.state = "run"
            self.stop_frame = False
        if dx == 0:
            self.state = "idle"
            if not self.stop_frame:
                self.frame = 0
                self.stop_frame = True
            
        self.x_pos += dx * self.speed * del_time
        self.rect.x = int(self.x_pos)
        self.start_time = cur_time
        
    def update(self):
        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.update_time) / 1000
        if del_time > const.ANIMATION_COOLDOWN:
            if self.frame < len(self.animation[self.state]):
                self.image = self.animation[self.state][self.frame]
                self.frame += 1
            else:
                self.frame = 0
            self.update_time = cur_time