"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame


class SpriteSheet:
    """ Class used to grab images out of a sprite sheet. """

    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # create a new blank image
        image = pygame.Surface([width, height]).convert()

        # copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey(pygame.Color(0, 0, 0))

        # return the image
        return image
