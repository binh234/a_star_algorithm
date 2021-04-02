from block import BlockType
from heapq import *
from math import sqrt

class Pathfinder:
    def __init__(self, grid):
        self.grid_object = grid

    @staticmethod
    def get_distance(block_a, block_b):
        ''' 
        Calculate distance a block to another block. This function is used to
        calculate both g and h distance for the problem

        Parameters:
            - block_a(Block): first block
            - block_b(Block): second block
        
        '''
        dist_x = abs(block_a.x - block_b.x)
        dist_y = abs(block_a.y - block_b.y)

        # if dist_x > dist_y:
        #     return 10 * dist_x + 4 * dist_y

        # return 10 * dist_y + 4 * dist_x
        return sqrt(dist_x * dist_x + dist_y * dist_y)

    def retrace_path(self, start, end):
        ''' 
        Trace path from source block to destination block

        Parameters:
            - start(Block): source block
            - end(Block): destination block
        
        '''
        path = []
        current_block = end

        while not current_block == start:
            path.append(current_block)
            current_block = current_block.parent

        path.append(start)

        [block.set_path() for block in path]

    def a_star_search(self, draw, start_block, end_block):
        ''' 
        Find the shortest path between a given source block
        to a destination block using A* Search Algorithm

        Parameters:
            - draw(function): utility function to draw block on the screen
            - start_block(Block): source block
            - end_block(Block): destination block
        
        '''

        # Initialize open list and closed list for A* algorithm
        open_list = []
        closed_list = set()

        # Add start block to the open list
        heappush(open_list, start_block)

        # Loop until open list is empty
        while len(open_list) > 0:
            # Extract the block with lowest f cost from
            # open list then add it to the closed list
            current_block = heappop(open_list)

            closed_list.add(current_block.position)
            current_block.set_closed()
            draw(current_block)

            # If the block is destination block then retrace path from source to destination
            if current_block.position == end_block.position:
                self.retrace_path(start_block, end_block)
                return

            # Get all successor (neighbor) of the current block
            for neighbour in self.grid_object.get_neighbours(current_block):
                # If the successor is bloked or is already in the closed list, then ignore it
                if neighbour.type == BlockType.WALL:
                    continue
                if neighbour.position in closed_list:
                    continue

                # Calculate g cost for the successor
                new_cost_to_neighbour = current_block.gCost + self.get_distance(current_block, neighbour)

                # If the successor is already in the open list and has a lower g cost
                # then update g cost for it. Notice that the h distance from a block
                # to the destination will never change, we don't have to update h cost
                if new_cost_to_neighbour < neighbour.gCost:
                    neighbour.gCost = new_cost_to_neighbour
                    neighbour.fCost = neighbour.gCost + neighbour.hCost
                    neighbour.parent = current_block

                # Else add the successor to the open list if it isn't in the open list
                elif neighbour.gCost == 0:
                    neighbour.gCost = new_cost_to_neighbour
                    neighbour.hCost = self.get_distance(neighbour, end_block)
                    neighbour.fCost = neighbour.gCost + neighbour.hCost
                    neighbour.parent = current_block
                    heappush(open_list, neighbour)
                    neighbour.set_open()
                    draw(neighbour)
