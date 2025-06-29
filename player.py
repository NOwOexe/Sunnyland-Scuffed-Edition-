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
        self.gravity_time = pygame.time.get_ticks()
        self.speed = const.PLAYER_SPEED
        self.velocity_y = 0
        self.x_pos = float(x)
        self.y_pos = float(y)
        self.is_flipped = False
        self.is_moving = False
        self.state = "idle"
        self.stop_frame = False
        self.is_ground = True
        self.is_jumping = False
    
    def draw(self, screen):
        flipped_img = pygame.transform.flip(self.image, self.is_flipped, False)
        screen.blit(flipped_img, (self.rect.x - const.PLAYER_OFFSET_X, self.rect.y - const.PLAYER_OFFSET_Y))
        pygame.draw.rect(screen, const.G_COLOR, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 1)
        
    def move(self):
        dx = 0
        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.start_time) / 1000
        delta_gravity = (cur_time - self.gravity_time) / 1000
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.is_flipped = True
            dx = -1
        if key[pygame.K_d]:
            self.is_flipped = False
            dx = 1
        if key[pygame.K_SPACE]:
            self.state = "jump"
            self.jump()
        if dx != 0 and self.is_jumping == False:
            if self.is_ground:
                self.state = "run"
            self.state = "run"
            self.stop_frame = False
        if dx == 0 and self.is_jumping == False:
            if self.is_ground:
                self.state = "idle"
            if not self.stop_frame:
                self.frame = 0
                self.stop_frame = True
            
        self.x_pos += dx * self.speed * del_time
        self.rect.x = int(self.x_pos)
        self.y_pos += self.velocity_y * delta_gravity
        self.rect.y = int(self.y_pos)
        if self.rect.y >= const.SCREEN_H - self.rect.h:
            self.is_ground = True
            self.is_jumping = False
            self.velocity_y = 0
        if not self.is_ground:
            self.velocity_y += const.GRAVITY
        self.start_time = cur_time
        self.gravity_time = cur_time
        
    def update(self):
        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.update_time) / 1000
        if del_time > const.ANIMATION_COOLDOWN:
            if self.frame < len(self.animation[self.state]) and not self.is_jumping:
                self.image = self.animation[self.state][self.frame]
                self.frame += 1
            else:
                self.frame = 0
            self.update_time = cur_time
            
    def jump(self):
        if self.is_ground:
            self.velocity_y = const.PLAYER_JUMPFORCE
            self.is_ground = False