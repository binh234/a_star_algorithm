import pygame
from enum import Enum

# Define all block types
class BlockType(Enum):
    DEFAULT = 1
    WALL = 2
    START = 3
    END = 4
    OPEN = 5
    CLOSED = 6
    PATH = 7


# Match each block type to the associate color
type_color = {
    BlockType.DEFAULT: [128, 128, 128],
    BlockType.WALL: [0, 0, 0],
    BlockType.START: [0, 255, 255],
    BlockType.END: [255, 165, 0],
    BlockType.OPEN: [0, 255, 0],
    BlockType.CLOSED: [255, 0, 0],
    BlockType.PATH: [0, 0, 255],
}


class Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * width + 1
        self.y = row * width + 1
        self.width = width
        self.type = BlockType.DEFAULT
        self.position = (row, col)

        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.parent = None

        self.rect = pygame.Rect(self.x, self.y, width-1, width-1)

    def get_rect(self):
        return self.rect

    def reset(self):
        """ Reset block """
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.parent = None
        self.type = BlockType.DEFAULT

    def set_default(self):
        """ Set block type to DEFAULT """
        self.type = BlockType.DEFAULT

    def set_wall(self):
        """ Set block type to WALL"""
        self.type = BlockType.WALL

    def set_start(self):
        """ Set block type to START """
        self.type = BlockType.START

    def set_end(self):
        """ Set block type to END """
        self.type = BlockType.END

    def set_closed(self):
        """ Set block type to CLOSED """
        self.type = BlockType.CLOSED

    def set_open(self):
        """ Set block type to OPEN """
        self.type = BlockType.OPEN

    def set_path(self):
        """ Set block type to PATH """
        self.type = BlockType.PATH
    
    def collidepoint(self, x, y):
        """ Check if the block contains point (x, y)"""
        return self.rect.collidepoint(x, y)

    def draw(self, screen):
        """ Draw block to the screen """
        pygame.draw.rect(screen, type_color[self.type], self.rect)

    def __lt__(self, other):
        if self.fCost < other.fCost:
            return True
        elif self.fCost == other.fCost:
            return self.hCost < other.hCost
        else:
            return False