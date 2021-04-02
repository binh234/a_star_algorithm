import pygame
from enum import Enum


class BlockType(Enum):
    DEFAULT = 1
    WALL = 2
    START = 3
    END = 4
    OPEN = 5
    CLOSED = 6
    PATH = 7


type_color = {
    BlockType.DEFAULT: [128, 128, 128],
    BlockType.WALL: [0, 0, 0],
    BlockType.START: [0, 255, 255],
    BlockType.END: [255, 165, 0],
    BlockType.OPEN: [0, 255, 0],
    BlockType.CLOSED: [255, 0, 0],
    BlockType.PATH: [255, 0, 255],
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
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.parent = None
        self.type = BlockType.DEFAULT

    def set_default(self):
        self.type = BlockType.DEFAULT

    def set_wall(self):
        self.type = BlockType.WALL

    def set_start(self):
        self.type = BlockType.START

    def set_end(self):
        self.type = BlockType.END

    def set_closed(self):
        self.type = BlockType.CLOSED

    def set_open(self):
        self.type = BlockType.OPEN

    def set_path(self):
        self.type = BlockType.PATH
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, type_color[self.type], self.rect)

    def __lt__(self, other):
        return self.fCost < other.fCost