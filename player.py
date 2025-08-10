import pygame
import constant as const

class Player():
    def __init__(self, animation, x, y):
        self.image = animation["idle"][0]
        self.animation = animation
        self.rect = self.image.get_rect(x=x, y=y)
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
        self.prev_rect = self.rect.copy()
        self.was_ground = False
        self.is_ground = False
        self.is_jumping = False
        self.move_dir = 0

        self.is_flipped = False
        self.is_moving = False
        self.state = "idle"
        self.stop_frame = False

    def draw(self, screen, camera):
        flipped_img = pygame.transform.flip(self.image, self.is_flipped, False)
        sx = self.rect.x - const.PLAYER_OFFSET_X - camera.offset.x
        sy = self.rect.y - const.PLAYER_OFFSET_Y - camera.offset.y
        screen.blit(flipped_img, (sx, sy))
        # debug rect
        debug_rect = self.rect.move(-camera.offset.x, -camera.offset.y)
        pygame.draw.rect(screen, const.G_COLOR, debug_rect, 1)


    def decide_state(self):
        if not self.is_ground:
            new_state = "jump"
        else:
            new_state = "idle" if self.move_dir == 0 else "run"
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

    def move(self):
        self.prev_rect = self.rect.copy()
        self.was_ground = self.is_ground
        self.is_ground = False

        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.start_time) / 1000.0
        delta_gravity = (cur_time - self.gravity_time) / 1000.0

        key = pygame.key.get_pressed()
        left = key[pygame.K_a]
        right = key[pygame.K_d]
        self.move_dir = (1 if right else 0) - (1 if left else 0)
        if self.move_dir < 0:
            self.is_flipped = True
        elif self.move_dir > 0:
            self.is_flipped = False

        if key[pygame.K_SPACE]:
            self.jump()

        self.x_pos += self.move_dir * self.speed * del_time
        self.rect.x = int(self.x_pos)

        self.y_pos += self.velocity_y * delta_gravity
        self.rect.y = int(self.y_pos)
        
        if self.rect.y >= const.SCREEN_H - self.rect.h:
            self.rect.y = const.SCREEN_H - self.rect.h
            self.y_pos = float(self.rect.y)
            self.velocity_y = 0
            self.is_ground = True
            self.is_jumping = False
            
        if not self.is_ground:
            self.velocity_y += const.GRAVITY * const.FPS_TARGET * delta_gravity

        self.is_jumping = not self.is_ground

        self.start_time = cur_time
        self.gravity_time = cur_time

    def update(self):
        self.decide_state()

        cur_time = pygame.time.get_ticks()
        del_time = (cur_time - self.update_time) / 1000.0
        if del_time > const.ANIMATION_COOLDOWN:
            if self.state == "jump":
                if self.frame < len(self.animation[self.state]):
                    self.image = self.animation[self.state][self.frame]
                    self.frame += 1
                else:
                    self.frame = len(self.animation[self.state]) - 1
                    self.image = self.animation[self.state][self.frame]
            else:
                # Loop run/idle
                if self.frame < len(self.animation[self.state]):
                    self.image = self.animation[self.state][self.frame]
                    self.frame += 1
                else:
                    self.frame = 0
                    self.image = self.animation[self.state][self.frame]
            self.update_time = cur_time

    def jump(self):
        if self.was_ground:
            self.velocity_y = const.PLAYER_JUMPFORCE
            self.is_ground = False
            self.is_jumping = True
            if self.state != "jump":
                self.state = "jump"
                self.frame = 0
            self.y_pos -= 1
            self.rect.y = int(self.y_pos)

    def check_collide(self, collidable):
        landed = False

        for tiles in collidable:
            if self.rect.colliderect(tiles):
                if self.prev_rect.bottom <= tiles.top and self.rect.bottom > tiles.top and self.velocity_y >= 0:
                    self.rect.bottom = tiles.top
                    self.y_pos = float(self.rect.y)
                    self.velocity_y = 0
                    self.is_ground = True
                    self.is_jumping = False
                    landed = True
                elif self.prev_rect.top >= tiles.bottom and self.rect.top < tiles.bottom:
                    self.rect.top = tiles.bottom
                    self.y_pos = float(self.rect.y)
                    self.velocity_y = 0
                elif self.prev_rect.right <= tiles.left and self.rect.right > tiles.left:
                    self.rect.right = tiles.left
                    self.x_pos = float(self.rect.x)
                elif self.prev_rect.left >= tiles.right and self.rect.left < tiles.right:
                    self.rect.left = tiles.right
                    self.x_pos = float(self.rect.x)

        if not landed:
            feet = self.rect.copy()
            FEET_TOL = 2
            feet.height += FEET_TOL

            for tiles in collidable:
                if (feet.colliderect(tiles)
                    and self.velocity_y >= 0
                    and self.rect.right > tiles.left and self.rect.left < tiles.right
                    and abs(self.rect.bottom - tiles.top) <= FEET_TOL):
                    self.rect.bottom = tiles.top
                    self.y_pos = float(self.rect.y)
                    self.velocity_y = 0
                    self.is_ground = True
                    self.is_jumping = False
                    landed = True
                    break

        if not landed and self.velocity_y != 0:
            self.is_ground = False

        self.decide_state()

