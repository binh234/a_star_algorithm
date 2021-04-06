import pygame
from block import BlockType
from board import Board
from pathfinder import Pathfinder
from tkinter import *
from tkinter import messagebox
import time
from threading import Thread

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
        self.board = Board(WINDOW_WIDTH, WINDOW_HEIGHT - 120, BLOCK_SIZE)
        self.finder = Pathfinder(self.board)

    def new_game(self, random=False):
        """ Restart for new game"""
        wall_percent = 0.4 if random else None
        self.started = False
        self.board.reset(wall_percent)

        self.screen.fill((255, 255, 255))
        self.draw_instruction()
        self.board.draw_board(self.screen)

    def draw_instruction(self):
        """ Draw game instructions"""
        font = self.font
        text_start = font.render("1: Switch pencil to draw starting point", 1, (0, 0, 0))
        text_end = font.render("2: Switch pencil to draw ending point", 1, (0, 0, 0))
        text_wall = font.render("3: Switch pencil to draw obstacles", 1, (0, 0, 0))
        text_eraser = font.render("RIGHT CLICK: Use eraser", 1, (0, 0, 0))

        text_run = font.render("SPACE: Start the A* algorithm with the current layout", 1, (0, 0, 0))
        text_new = font.render("N: New game", 1, (0, 0, 0))
        text_random = font.render("R: Random game", 1, (0, 0, 0))
        text_quit = font.render("Q: Quit game", 1, (0, 0, 0))

        self.screen.blit(text_start, (20, 690))
        self.screen.blit(text_end, (20, 715))       
        self.screen.blit(text_wall, (20, 740))   
        self.screen.blit(text_eraser, (20, 765))    

        self.screen.blit(text_run, (800, 690))
        self.screen.blit(text_new, (800, 715))
        self.screen.blit(text_random, (800, 740))
        self.screen.blit(text_quit, (800, 765))

    def run(self):
        self.new_game()
        self.is_running = True
        screen = self.screen

        # Main loop
        while self.is_running:
            # Get event from keyboard and mouse click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    # N => new game
                    if event.key == pygame.K_n:
                        self.new_game()
                    # R => random game
                    elif event.key == pygame.K_r:
                        self.new_game(random=True)
                    # Q => quit game
                    elif event.key == pygame.K_q:
                        self.is_running = False

                if not self.started:
                    # If left mouse clicked, draw on the selected block
                    if pygame.mouse.get_pressed()[0]:
                        # Find the clicked clock
                        block = self.board.find_collide_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if block:
                            # Draw start block
                            if self.pencil == BlockType.START:
                                found, start_block = self.board.find_start()
                                if found:
                                    start_block.set_default()
                                    self.board.redraw(start_block, screen)
                                block.set_start()
                                self.board.redraw(block, screen)
                            # Draw end block
                            elif self.pencil == BlockType.END:
                                found, end_block = self.board.find_end()
                                if found:
                                    end_block.set_default()
                                    self.board.redraw(end_block, screen)
                                block.set_end()
                                self.board.redraw(block, screen)
                            # Draw wall block
                            else:
                                block.set_wall()
                                self.board.redraw(block, screen)

                    # If right mouse clicked, erase the current selected block if it is already drew
                    elif pygame.mouse.get_pressed()[2]:
                        block = self.board.find_collide_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if block:
                            block.set_default()
                            self.board.redraw(block, screen)

                    if event.type == pygame.KEYDOWN:
                        # 1 => switch pencil to draw start block
                        if event.key == pygame.K_1:
                            self.pencil = BlockType.START
                        # 2 => switch pencil to draw end block
                        elif event.key == pygame.K_2:
                            self.pencil = BlockType.END
                        # 3 => switch pencil to draw wall block
                        elif event.key == pygame.K_3:
                            self.pencil = BlockType.WALL
                        # SPACE => start game
                        elif event.key == pygame.K_SPACE:
                            found_start, start_block = self.board.find_start()
                            found_end, end_block = self.board.find_end()
                            # Start game if and only if there are a start and end block on the board
                            if found_start and found_end:
                                self.started = True

                                args = [lambda block: self.board.redraw(block, screen), start_block, end_block]
                                success = self.finder.a_star_search(*args)

                                if success:
                                    self.board.draw_path(screen)
                                else:
                                    Tk().wm_withdraw()  # to hide the main window
                                    messagebox.showinfo('ERROR', 'No solution!!!')
                            else:
                                Tk().wm_withdraw()  # to hide the main window
                                messagebox.showinfo('ERROR', 'Please select a start and end point')

        self.quit()

    def quit(self):
        pygame.quit()
        quit()