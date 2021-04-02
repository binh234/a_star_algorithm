import pygame
from block import BlockType
import grid as g
from pathfinder import Pathfinder
from tkinter import *
from tkinter import messagebox
import time

# SIZE VARIABLES
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 800
BLOCK_SIZE = 20

class Game():
    def __init__(self):
        # INIT PYGAME
        pygame.init()
        pygame.display.set_caption("A* demo")
        pygame.font.init()

        self.font = pygame.font.SysFont("roboto", 25)

        self.is_running = False
        self.started = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pencil = BlockType.WALL
        self.grid = g.Grid(WINDOW_WIDTH, WINDOW_HEIGHT - 120, BLOCK_SIZE)

    def new_game(self):
        self.started = False
        self.grid.reset()

        self.screen.fill((255, 255, 255))
        self.draw_instruction()
        self.grid.draw_grid(self.screen)

    def draw_instruction(self):
        font = self.font
        text_start = font.render("1: Switch pencil to draw starting point", 1, (0, 0, 0))
        text_end = font.render("2: Switch pencil to draw ending point", 1, (0, 0, 0))
        text_wall = font.render("3: Switch pencil to draw obstacles", 1, (0, 0, 0))

        text_run = font.render("SPACE: Start the A* algorithm with the current layout", 1, (0, 0, 0))
        text_reset = font.render("R: Start new game", 1, (0, 0, 0))
        text_eraser = font.render("RIGHT CLICK: Use eraser", 1, (0, 0, 0))

        self.screen.blit(text_start, (20, 700))
        self.screen.blit(text_end, (20, 730))       
        self.screen.blit(text_wall, (20, 760))       

        self.screen.blit(text_run, (800, 700))
        self.screen.blit(text_reset, (800, 730))
        self.screen.blit(text_eraser, (800, 760))

    def run(self):
        self.new_game()
        self.is_running = True
        screen = self.screen

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.new_game()
                    elif event.key == pygame.K_q:
                        self.is_running = False

                if not self.started:
                    if pygame.mouse.get_pressed()[0]:
                        block = self.grid.find_collide_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if block:
                            if self.pencil == BlockType.START:
                                found, start_block = self.grid.find_start()
                                if found:
                                    start_block.set_default()
                                    self.grid.redraw(start_block, screen)
                                block.set_start()
                                self.grid.redraw(block, screen)
                            elif self.pencil == BlockType.END:
                                found, end_block = self.grid.find_end()
                                if found:
                                    end_block.set_default()
                                    self.grid.redraw(end_block, screen)
                                block.set_end()
                                self.grid.redraw(block, screen)
                            else:
                                block.set_wall()
                                self.grid.redraw(block, screen)

                    elif pygame.mouse.get_pressed()[2]:
                        block = self.grid.find_collide_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if block:
                            block.set_default()
                            self.grid.redraw(block, screen)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.pencil = BlockType.START
                        elif event.key == pygame.K_2:
                            self.pencil = BlockType.END
                        elif event.key == pygame.K_3:
                            self.pencil = BlockType.WALL
                        elif event.key == pygame.K_SPACE:
                            found_start, start_block = self.grid.find_start()
                            found_end, end_block = self.grid.find_end()
                            if found_start and found_end:
                                # a = time.time()
                                self.started = True
                                finder = Pathfinder(self.grid)
                                finder.a_star_search(lambda block: self.grid.redraw(block, screen), start_block, end_block)
                                self.grid.draw_path(screen)
                                # c = time.time()
                                # Tk().wm_withdraw()  # to hide the main window
                                # messagebox.showinfo('PERFORMANCE', c-a)
                            else:
                                Tk().wm_withdraw()  # to hide the main window
                                messagebox.showinfo('ERROR', 'Please select a start and end point')

        pygame.quit()
        quit()