import math
import pygame
import constant as const


def _get_offset(camera):
    if camera is not None:
        return pygame.Vector2(camera.offset.x, camera.offset.y)
    return pygame.Vector2(0, 0)

class Enemy:
    def __init__(self, animation, x, y, state: str):
        self.image = animation[state][0]
        self.animation = animation
        self.rect = self.image.get_rect(x=x, y=y)
        self.state = state
        self.frame = 0
        self.anim_time = pygame.time.get_ticks()
        self.flipped = False
        
        self.alive = True
        
    def kill(self):
        self.alive = False

    def draw(self, screen: pygame.Surface, camera):
        if not self.alive:
            return
        off = _get_offset(camera)
        flipped_image = pygame.transform.flip(self.image, self.flipped, False)
        screen.blit(flipped_image, (self.rect.x - off.x, self.rect.y - off.y))
        # debug collider :))))
        pygame.draw.rect(screen, const.G_COLOR,
                         pygame.Rect(self.rect.x - off.x, self.rect.y - off.y, self.rect.w, self.rect.h), 1)

    def update(self):
        cur = pygame.time.get_ticks()
        if (cur - self.anim_time) / 1000.0 > const.ANIMATION_COOLDOWN:
            frames = self.animation[self.state]
            if self.frame < len(frames):
                self.image = frames[self.frame]
                self.frame += 1
            else:
                self.frame = 0
                self.image = frames[self.frame]
            self.anim_time = cur


class Slime(Enemy):
    def __init__(self, animation, x, y, state: str):
        super().__init__(animation, x, y, state)
        self.offset_x = const.SLIME_OFFSET_X
        self.offset_y = const.SLIME_OFFSET_Y
        self.offset_w = const.SLIME_OFFSET_W
        self.offset_h = const.SLIME_OFFSET_H
        self.rect.w -= self.offset_w
        self.rect.h -= self.offset_h
        self.is_ground = False
        self.start_time = pygame.time.get_ticks()

        self.aggro_rect = pygame.Rect(
            x - (const.AGGRO_W - self.rect.w) / 2,
            y - const.AGGRO_H / 2 + 16,
            const.AGGRO_W,
            const.AGGRO_H,
        )
        self.x_pos = float(self.rect.x)
        self.aggro_pos = float(self.aggro_rect.x)

    def draw(self, screen: pygame.Surface, camera):
        off = _get_offset(camera)
        flipped_image = pygame.transform.flip(self.image, self.flipped, False)
        screen.blit(flipped_image, (self.rect.x - self.offset_x - off.x,
                                    self.rect.y - self.offset_y - off.y))
        # debug :))))))))))
        pygame.draw.rect(screen, const.G_COLOR,
                         pygame.Rect(self.rect.x - off.x, self.rect.y - off.y, self.rect.w, self.rect.h), 1)
        pygame.draw.rect(screen, const.B_COLOR,
                         pygame.Rect(self.aggro_rect.x - off.x, self.aggro_rect.y - off.y,
                                     self.aggro_rect.w, self.aggro_rect.h), 1)

    def move(self, player, delta_time: float):
        if player.rect.colliderect(self.aggro_rect):
            self.state = "run"
            if player.rect.x >= self.rect.x:
                self.flipped = True
                self.x_pos += const.SLIME_SPEED * delta_time
                self.aggro_pos += const.SLIME_SPEED * delta_time
            else:
                self.flipped = False
                self.x_pos -= const.SLIME_SPEED * delta_time
                self.aggro_pos -= const.SLIME_SPEED * delta_time
            self.rect.x = int(self.x_pos)
            self.aggro_rect.x = int(self.aggro_pos)
        else:
            self.state = "idle"
            
    def check_collide(self, collideable):
        for tiles in collideable:
            if self.rect.colliderect(tiles):
                self.is_ground = True
                self.rect.bottom = tiles.top
                self.aggro_rect.y = self.rect.y
                self.aggro_rect.bottom = tiles.top
    
    def gravity(self, collidable):
        cur_time = pygame.time.get_ticks()
        delta_gravity = (cur_time - self.start_time) / 1000.0
        if not self.is_ground:
            self.rect.y += const.GRAVITY * const.FPS_TARGET * delta_gravity
        

class Bat(Enemy):
    def __init__(self, animation, x, y, state: str):
        super().__init__(animation, x, y, state)
        self.base_y = float(self.rect.y)
        self.amp = 100.0
        self.omega = (const.BAT_FLY_SPEED / self.amp) if self.amp != 0 else 0.0
        self.phase = 0.0
        self.y_pos = float(self.rect.y)

    def move(self, delta_time: float):
        self.phase += self.omega * delta_time
        self.y_pos = self.base_y + self.amp * math.sin(self.phase)
        self.rect.y = int(self.y_pos)


class Frog(Enemy):

    def __init__(self, animation, x, y, state: str):
        super().__init__(animation, x, y, state)
        self.min_dx = self.rect.x - 100
        self.max_dx = self.rect.x + 100

        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)
        self.vx = 0.0
        self.vy = 0.0
        self.direction = 1  
        self.is_ground = False
        self.prev_rect = self.rect.copy()

        self.jump_cooldown = 0.0
        self._land_time = pygame.time.get_ticks()

        self.state = "idle"
        self._jump_frame_idx = 0

    def _start_jump(self):
        self.vy = const.FROG_JUMPFORCE
        self.vx = const.FROG_SPEED * self.direction
        self.state = "jump"

    def _choose_direction_from_bounds(self):
        cx = self.rect.centerx
        TOL = 2
        if cx >= self.max_dx - TOL:
            self.direction = -1
        elif cx <= self.min_dx + TOL:
            self.direction = 1
        self.flipped = True if self.direction == 1 else False

    def _feet_probe(self, tiles: pygame.Rect) -> bool:
        FEET_TOL = 2
        if (self.vy >= 0 and
            self.rect.right > tiles.left and self.rect.left < tiles.right and
            abs(self.rect.bottom - tiles.top) <= FEET_TOL):
            self.rect.bottom = tiles.top
            self.y_pos = float(self.rect.y)
            self.vy = 0.0
            self.is_ground = True
            self.state = "idle"
            return True
        return False

    def _collide(self, collidable):
        landed = False
        for tiles in collidable:
            if self.rect.colliderect(tiles):
                if self.prev_rect.bottom <= tiles.top and self.rect.bottom > tiles.top and self.vy >= 0:
                    self.rect.bottom = tiles.top
                    self.y_pos = float(self.rect.y)
                    self.vy = 0.0
                    self.is_ground = True
                    self.state = "idle"
                    landed = True
                elif self.prev_rect.top >= tiles.bottom and self.rect.top < tiles.bottom and self.vy < 0:
                    self.rect.top = tiles.bottom
                    self.y_pos = float(self.rect.y)
                    self.vy = 0.0
                elif self.prev_rect.right <= tiles.left and self.rect.right > tiles.left:
                    self.rect.right = tiles.left
                    self.x_pos = float(self.rect.x)
                    self.direction = -1
                    self.flipped = False
                elif self.prev_rect.left >= tiles.right and self.rect.left < tiles.right:
                    self.rect.left = tiles.right
                    self.x_pos = float(self.rect.x)
                    self.direction = 1
                    self.flipped = True

        if not landed:
            for tiles in collidable:
                if self._feet_probe(tiles):
                    landed = True
                    break

        if not landed and self.vy != 0:
            self.is_ground = False

    def move(self, collidable, delta_time: float):
        self.prev_rect = self.rect.copy()

        if self.is_ground and self.state != "jump":
            self._choose_direction_from_bounds()
            if (pygame.time.get_ticks() - self._land_time) / 1000.0 >= self.jump_cooldown:
                self._start_jump()

        self.x_pos += self.vx * delta_time
        self.y_pos += self.vy * delta_time
        self.vy += const.GRAVITY

        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

        self._collide(collidable)

        if self.is_ground:
            self.vx = 0.0
            if self.state != "idle":
                self.state = "idle"
            self._land_time = pygame.time.get_ticks()

        if not self.is_ground:
            self._choose_direction_from_bounds()

    def update(self):
        if self.state == "jump":
            vy = self.vy
            EPS = 5.0
            if vy < -EPS:
                self._jump_frame_idx = 0
            elif vy > EPS:
                self._jump_frame_idx = 1
            frames = self.animation.get("jump", [])
            if frames:
                idx = min(self._jump_frame_idx, len(frames) - 1)
                self.image = frames[idx]
            self.anim_time = pygame.time.get_ticks()
            return

        super().update()

