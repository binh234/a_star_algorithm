import block as b
import pygame

class Grid:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.rows = height // size
        self.cols = width // size
        self.block_size = size
        self.grid = self.create_grid()
        self.currentBlock = self.grid[0][0]

    def create_grid(self):
        grid = []
        for x in range(self.rows):
            row = []
            for y in range(self.cols):
                item = b.Block(x, y, self.block_size)
                row.append(item)

            grid.append(row)
        return grid

    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].reset()

    def get_neighbours(self, block):
        neighbours = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                else:
                    check_x = block.row + x
                    check_y = block.col + y

                    if check_x >= 0 and check_x < self.rows and check_y >= 0 and check_y < self.cols:
                        neighbours.append(self.grid[check_x][check_y])

        return neighbours

    def draw_grid(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].draw(screen)

        for x in range(0, self.width, self.block_size):
            pygame.draw.line(screen, [212, 212, 212], (x, 0), (x, self.height))
        for y in range(self.block_size, self.height + 1, self.block_size):
            pygame.draw.line(screen, [212, 212, 212], (0, y), (self.width, y))

        pygame.draw.line(screen, [212, 212, 212], (self.width + self.block_size, 0), (self.width + self.block_size, self.height))

        pygame.display.update()

    def draw_path(self, screen):
        for row in self.grid:
            for block in row:
                if block.type == b.BlockType.OPEN or block.type == b.BlockType.CLOSED:
                    block.set_default()
        self.draw_grid(screen)
    
    def redraw(self, block, screen):
        block.draw(screen)
        pygame.display.update()
    
    def find_collide_block(self, x, y):
        row = y // self.block_size
        col = x // self.block_size
        if row < self.rows and col < self.cols and self.grid[row][col].collidepoint(x, y):
            return self.grid[row][col]
        
        return None
    
    def find_block(self, block_type):
        for row in self.grid:
            for block in row:
                if block.type == block_type:
                    return True, block
        
        return False, None

    def find_start(self):
        return self.find_block(b.BlockType.START)

    def find_end(self):
        return self.find_block(b.BlockType.END)
