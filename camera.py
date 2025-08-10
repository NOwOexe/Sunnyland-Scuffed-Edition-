import pygame
import math

class Camera:
    def __init__(self, screen_size, world_size, deadzone=(300, 180)):
        self.sw, self.sh = screen_size
        self.ww, self.wh = world_size
        self.offset = pygame.Vector2(0, 0)

        dz_w, dz_h = deadzone
        self.deadzone = pygame.Rect((self.sw - dz_w)//2, (self.sh - dz_h)//2, dz_w, dz_h)

    def update(self, target_rect: pygame.Rect):
        px = target_rect.x - self.offset.x
        py = target_rect.y - self.offset.y

        if px < self.deadzone.left:
            self.offset.x = target_rect.x - self.deadzone.left
        elif px + target_rect.w > self.deadzone.right:
            self.offset.x = target_rect.x + target_rect.w - self.deadzone.right

        if py < self.deadzone.top:
            self.offset.y = target_rect.y - self.deadzone.top
        elif py + target_rect.h > self.deadzone.bottom:
            self.offset.y = target_rect.y + target_rect.h - self.deadzone.bottom

        self.offset.x = max(0, min(self.offset.x, self.ww - self.sw))
        self.offset.y = max(0, min(self.offset.y, self.wh - self.sh))

    def apply(self, rect_or_xy):
        if isinstance(rect_or_xy, pygame.Rect):
            return rect_or_xy.move(-self.offset.x, -self.offset.y)
        x, y = rect_or_xy
        return (x - self.offset.x, y - self.offset.y)
