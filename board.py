import block as b
import pygame
import random

class Board:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.rows = height // size
        self.cols = width // size
        self.block_size = size
        self.grid = self.create_grid()

    def create_grid(self):
        """ Create board grid"""
        grid = []
        for x in range(self.rows):
            row = []
            for y in range(self.cols):
                item = b.Block(x, y, self.block_size)
                row.append(item)

            grid.append(row)
        return grid

    def reset(self, wall_percent=None):
        """ Reset the board to start new game"""
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].reset()
                if wall_percent is not None: # Random game
                    if random.random() < wall_percent:
                        self.grid[row][col].set_wall()


        if wall_percent is not None: # Random game            
            start_row, start_col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            end_row, end_col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            while end_row == start_row and end_col == start_col:
                end_row, end_col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)

            self.grid[start_row][start_col].set_start()
            self.grid[end_row][end_col].set_end()

    def get_neighbors(self, block):
        """ Find all neighbors of a block"""
        neighbors = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                else:
                    check_x = block.row + x
                    check_y = block.col + y

                    if check_x >= 0 and check_x < self.rows and check_y >= 0 and check_y < self.cols:
                        neighbors.append(self.grid[check_x][check_y])

        return neighbors

    def draw_board(self, screen):
        """ Draw board on the screen"""

        # Draw all blocks in the board
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].draw(screen)

        # Draw lines
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(screen, [212, 212, 212], (x, 0), (x, self.height))
        for y in range(self.block_size, self.height + 1, self.block_size):
            pygame.draw.line(screen, [212, 212, 212], (0, y), (self.width, y))

        pygame.draw.line(screen, [212, 212, 212], (self.width + self.block_size, 0), (self.width + self.block_size, self.height))

        pygame.display.update()

    def draw_path(self, screen):
        """ Draw path when the A* aalgorithm finnished"""
        for row in self.grid:
            for block in row:
                if block.type == b.BlockType.OPEN or block.type == b.BlockType.CLOSED:
                    block.set_default()
        self.draw_board(screen)
    
    def redraw(self, block, screen):
        """ Update a block on the board"""
        block.draw(screen)
        pygame.display.update()
    
    def find_collide_block(self, x, y):
        """ Find the block that contains point (x, y) """
        row = y // self.block_size
        col = x // self.block_size
        if row < self.rows and col < self.cols and self.grid[row][col].collidepoint(x, y):
            return self.grid[row][col]
        
        return None
    
    def find_block(self, block_type):
        """ Find the first block that matches the block type"""
        for row in self.grid:
            for block in row:
                if block.type == block_type:
                    return True, block
        
        return False, None

    def find_start(self):
        """ Find the start block"""
        return self.find_block(b.BlockType.START)

    def find_end(self):
        """ Find the end block"""
        return self.find_block(b.BlockType.END)
