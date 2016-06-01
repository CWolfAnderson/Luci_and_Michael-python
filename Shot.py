import pygame
from spritesheet_functions import SpriteSheet

class Shot(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, shooter_name, direction, ix, iy, speed, damage, range, size):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.direction = direction

        # inherited x & y velocities
        if self.direction == "U" or self.direction == "D":
            self.ix = ix
        else:
            self.ix = 0

        if self.direction == "L" or self.direction == "R":
            self.iy = iy
        else:
            self.iy = 0

        self.speed = speed
        self.damage = damage
        self.range = range

        sprite_sheet = SpriteSheet("res/img/space.png")

        if shooter_name == "Luci":
            if self.direction == "U":
                image = sprite_sheet.get_image(74, 269, 27, 44)
                self.image = pygame.transform.scale(image, size[0])
            elif self.direction == "D":
                image = sprite_sheet.get_image(168, 269, 27, 44)
                self.image = pygame.transform.scale(image, size[0])
            elif self.direction == "L":
                image = sprite_sheet.get_image(112, 277, 44, 26)
                self.image = pygame.transform.scale(image, size[1])
            elif self.direction == "R":
                image = sprite_sheet.get_image(18, 277, 44, 26)
                self.image = pygame.transform.scale(image, size[1])
        else:
            if self.direction == "U":
                image = sprite_sheet.get_image(75, 314, 27, 44)
                self.image = pygame.transform.scale(image, size[0])
            elif self.direction == "D":
                image = sprite_sheet.get_image(168, 320, 27, 44)
                self.image = pygame.transform.scale(image, size[0])
            elif self.direction == "L":
                image = sprite_sheet.get_image(110, 324, 44, 26)
                self.image = pygame.transform.scale(image, size[1])
            elif self.direction == "R":
                image = sprite_sheet.get_image(20, 324, 44, 26)
                self.image = pygame.transform.scale(image, size[1])

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        if self.direction == "U":
            self.rect.y -= self.speed
        elif self.direction == "D":
            self.rect.y += self.speed
        elif self.direction == "L":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        # add the inherited velocity
        self.rect.x += self.ix
        self.rect.y += self.iy