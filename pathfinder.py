from block import BlockType
from heapq import *
from math import sqrt

class Pathfinder:
    def __init__(self, board):
        self.board_object = board

    @staticmethod
    def get_distance(block_a, block_b):
        ''' 
        Calculate distance a block to another block. This function is used to
        calculate both g and h distance for the problem

        Parameters:
            - block_a(Block): first block
            - block_b(Block): second block
        
        '''
        dist_x = abs(block_a.row - block_b.row)
        dist_y = abs(block_a.col - block_b.col)

        if dist_x > dist_y:
            return 1000 * dist_x + 414 * dist_y

        return 1000 * dist_y + 414 * dist_x
        # return sqrt(dist_x * dist_x + dist_y * dist_y)

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

        path[-1].set_start()
        [block.set_path() for block in path[1:-1]]
        path[0].set_end()

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
            # open list
            current_block = heappop(open_list)

            # If the current block is already in closed list, ignore it
            if current_block.position in closed_list:
                continue

            closed_list.add(current_block.position)
            current_block.set_closed()
            draw(current_block)

            # If the block is destination block then retrace path from source to destination
            if current_block.position == end_block.position:
                self.retrace_path(start_block, end_block)
                return True

            # Get all successor (neighbor) of the current block
            for neighbor in self.board_object.get_neighbors(current_block):
                # If the successor is bloked or is already in the closed list, then ignore it
                if neighbor.type == BlockType.WALL:
                    continue
                if neighbor.position in closed_list:
                    continue

                # Calculate g cost for the successor
                new_cost_to_neighbor = current_block.gCost + self.get_distance(current_block, neighbor)

                # If the successor is already in the open list and has a lower g cost
                # then update g cost for it. Note that the h distance from a block
                # to the destination will never change, we don't have to update h cost
                if new_cost_to_neighbor < neighbor.gCost:
                    neighbor.gCost = new_cost_to_neighbor
                    neighbor.fCost = neighbor.gCost + neighbor.hCost
                    neighbor.parent = current_block
                    heappush(open_list, neighbor)

                # Else add the successor to the open list if it isn't in the open list
                elif neighbor.gCost == 0:
                    neighbor.gCost = new_cost_to_neighbor
                    neighbor.hCost = self.get_distance(neighbor, end_block)
                    neighbor.fCost = neighbor.gCost + neighbor.hCost
                    neighbor.parent = current_block
                    heappush(open_list, neighbor)
                    neighbor.set_open()
                    draw(neighbor)

        return False
