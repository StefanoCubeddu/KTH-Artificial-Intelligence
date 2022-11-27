#!/usr/bin/env python3
import random
import math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import time


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object
        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3},
          'fish1': {'score': 2, 'type': 1},
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }
        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return MiniMax()



    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        initial_time = time.time()
        d = 0
        timeout = False
        hash = dict()
        best_move = 0

        while not timeout:
            try:
                move = model.ids(initial_tree_node, d, initial_time,hash)
                d += 1
                best_move = move
            except:
                timeout = True

        return ACTION_TO_STR[best_move]


class MiniMax:

    def hash_it(self, state):
        fish_pos= state.get_fish_positions()
        hook_pos = state.get_hook_positions()
        fish_score = state.get_fish_scores()
        composite_key = {
            "{:02d}{:02d}".format(fish_pos[0], fish_pos[1]): fish_score[fish_idx]
            for fish_idx, fish_pos in fish_pos.items()
        }
        return str(hook_pos) + str(composite_key)


    def get_heuristic_base(self,node):
        A_score,B_score=node.state.get_player_scores()
        v=A_score-B_score
        return v


    def heuristics(self, node):

        state = node.state
        score = self.get_heuristic_base(node)
        hook = state.hook_positions[0]
        h = 0
        for i, coord in state.fish_positions.items():
            h = max(h, state.fish_scores[i] * math.exp(-self.distance(hook, coord)))

        return 2.2 * score + h 


    def get_heuristic2(self,node):
        fish_position=node.state.get_fish_positions()
        fish_scores=node.state.get_fish_scores()
        pos=node.state.get_hook_positions()
        pos=pos[0]
        
        v=2*self.get_heuristic(node)
        for fish,score in zip(fish_position,fish_scores):
            distance=self.l1_distance(fish_position,pos,fish)
            if(not distance==0):
                v+=1/distance*fish_scores[fish] 
            else:
                v+=100 
        return v

       
    def distance(self, hook_pos, fish_pos):
        y = abs(fish_pos[1] - hook_pos[1])

        return y + min(abs(fish_pos[0] - hook_pos[0] + 20), abs(fish_pos[0] - hook_pos[0] - 20), abs(fish_pos[0] - hook_pos[0]))

    def mini_max(self, node, d, alpha, beta, player, initial_time,hash):
        if time.time() - initial_time > 0.047:
            raise TimeoutError
        else:
            k = self.hash_it(node.state)
            if k in hash and hash[k][0] >= d:
                return hash[k][1]
            moves = node.compute_and_get_children()
            moves.sort(key=self.heuristics, reverse = True)
            if d == 0 or len(moves) == 0:
                h = self.heuristics(node)
                
            elif player:
                h = float('-inf')
                for child in moves:
                    if(self.free_move(node,child.move,player)==True):
                        h = max(h, self.mini_max(child, d - 1, alpha, beta, False, initial_time,hash))
                        alpha = max(alpha, h)
                        if alpha >= beta:
                            break
            else:
                h = float('inf')
                for child in moves[::-1]:
                    if(self.free_move(node,child.move,player)==True):
                        h = min(h, self.mini_max(child, d - 1, alpha, beta, True, initial_time,hash))
                        beta = min(beta, h)
                        if alpha >= beta:
                            break

            # key = self.hash_it(node.state)
            hash.update({k:[d,h]})
        return h

        
    def free_move(self,node,move,player):
            x=-1
            if(player==True):
                x=0
            else:
                x=1
            pos=node.state.get_hook_positions()
            if(player=="A" and pos[1][0]-pos[0][0]==1 and move==4):
                    return False
            if(player=="B" and pos[0][0]-pos[1][0]==1 and move==4):
                    return False
            if(player=="A" and pos[0][0]-pos[1][0]==1 and move==3):
                    return False
            if(player=="B" and pos[1][0]-pos[0][0]==1 and move==3):
                    return False
            if(pos[x][1]==19 and move==2):
                    return False
            if(pos[x][1]==0 and move==1):
                    return False
            return True
        
    def ids(self, node, d, initial_time,hash):
        
        best_heur = []
        moves = node.compute_and_get_children()
        for child in moves:
            heur = self.mini_max(child, d, float('-inf'), float('inf'), False, initial_time,hash)
            best_heur.append(heur)

        best_heur_idx = best_heur.index(max(best_heur))
        return moves[best_heur_idx].move 

    
    def last_fish(self,node,child,fish_pos):    
        fish_pos=node.state.get_fish_positions()[0]
        hook_node=node.state.get_hook_positions()[0]
        hook_child=child.state.get_hook_positions()[0]
        if(self.l1_distance(hook_node,fish_pos)<(self.l1_distance(hook_child,fish_pos))):
            return True
        else:
            return False

       