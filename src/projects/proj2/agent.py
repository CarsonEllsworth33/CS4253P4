 #!/usr/bin/env python3

from ...lib.game import Agent, RandomAgent
import math

class MinimaxAgent(RandomAgent):
    """An agent that makes decisions using the Minimax algorithm, using a
    evaluation function to approximately guess how good certain states
    are when looking far into the future.

    :param evaluation_function: The function used to make evaluate a
        GameState. Should have the parameters (state, player_id) where
        `state` is the GameState and `player_id` is the ID of the
        player to calculate the expected payoff for.

    :param alpha_beta_pruning: True if you would like to use
        alpha-beta pruning.

    :param max_depth: The maximum depth to search using the minimax
        algorithm, before using estimates generated by the evaluation
        function.
    """
    def __init__(self, evaluate_function, alpha_beta_pruning=False, max_depth=5):
        super().__init__()
        self.evaluate = evaluate_function
        self.alpha_beta_pruning = alpha_beta_pruning
        self.max_depth = max_depth

    def decide(self, state):
        # TODO: Implement this agent!
        #
        # Read the documentation in /src/lib/game/_game.py for
        # information on what the decide function does.
        #
        # Do NOT call the soccer evaluation function that you write
        # directly from this function! Instead, use
        # `self.evaluate`. It will behave identically, but will be
        # able to work for multiple games.
        #
        # Do NOT call any SoccerState-specific functions! Assume that
        # you can only see the functions provided in the GameState
        # class.
        #
        # If you would like to see some example agents, check out
        # `/src/lib/game/_agents.py`.
        import time
        
        time_start = 0
        time_finish = 0
        if not self.alpha_beta_pruning:
            time_start = time.time()
            a = self.minimax(state,state.current_player)
            time_finish = time.time() - time_start
            print("time taken to decide",time_finish)
            print('\n')
            return a
        else:
            time_start = time.time()
            a = self.minimax_with_ab_pruning(state,state.current_player)
            time_finish = time.time() - time_start
            print("time taken to decide",time_finish)
            print('\n')
            return a
        
        
        
    def minimax(self, state, player,depth=1):
        # This is the suggested method you use to do minimax.  Assume
        # `state` is the current state, `player` is the player that
        # the agent is representing (NOT the current player in
        # `state`!)  and `depth` is the current depth of recursion.        
        
        min_man = False if state.current_player == player else True
        
        
       
        
        if depth >= 3 or state.is_terminal:
            v = self.evaluate(state,player)
            return v 
        
        
        #depth <= 2
        if min_man:
            v = math.inf
            l = []
            #for action in action_states:
            try:
                new_depth = depth + 1
                for action in state.actions:
                    #print("action", action)
                    if(state.act(action) != None):
                        val = self.minimax(state.act(action),player,new_depth)
                        a = min(v, val)
                        v = a if a != math.inf else v
                        x = val,action
                        l.append(x)
                
                if(v != math.inf):
                    return v
                
            except(AttributeError):
                pass
        
        else:
            v = -math.inf
            l = []
            #for action in action_states:
            try:
                new_depth = depth + 1
                for action in state.actions:
                    if(state.act(action) != None):
                        val = self.minimax(state.act(action),player,new_depth)
                        a = max(v, val)
                        v = a if a != math.inf else v
                        x = val,action
                        l.append(x)
                    
                
                if(v != math.inf):
                    if depth == 1:
                        try:
                            return max(l)[1]
                        except(TypeError):
                            return l[0][1]
                    else:
                        return v
            except(AttributeError):
                pass   
            

    def minimax_with_ab_pruning(self, state, player, depth=1,
                                alpha=float('inf'), beta=-float('inf')):
         # This is the suggested method you use to do minimax.  Assume
        # `state` is the current state, `player` is the player that
        # the agent is representing (NOT the current player in
        # `state`!)  and `depth` is the current depth of recursion.        
        
        min_man = False if state.current_player == player else True
        
        
       
        
        if depth >= 3 or state.is_terminal:
            v = self.evaluate(state,player)
            return v, alpha, beta
        
        
        #depth <= 2
        if min_man:
            v = math.inf
            l = []
            #for action in action_states:
            try:
                new_depth = depth + 1
                for action in state.actions:
                    #print("action", action)
                    if(state.act(action) != None):
                        val = self.minimax_with_ab_pruning(state.act(action),player,new_depth,alpha,beta)[0]
                        a = min(v, val)
                        v = a if a != math.inf else v
                        x = val,action
                        l.append(x)
                        #ab breakouts will happen here
                        ##############################
                        #if(beta != -math.inf):
                        if(val <= beta):
                            beta = val
                            break
                        #if val is bigger then beta then we must keep searching
                if(depth == 2):
                    beta = min(l)[0]
                
                
                if(v != math.inf):
                    return v , alpha, beta
                
            except(AttributeError):
                pass
        
        #depth = 1(root)
        else:
            v = -math.inf
            l = []
            #for action in action_states:
            try:
                new_depth = depth + 1
                for action in state.actions:
                    if(state.act(action) != None):
                        val = self.minimax_with_ab_pruning(state.act(action),player,new_depth,alpha,beta)[0]
                        a = max(v, val)
                        v = a if a != math.inf else v
                        x = val,action
                        l.append(x)
                        #ab breakouts will happen here
                        ##############################
                        #if (alpha != math.inf):
                        if(val >= alpha):
                            alpha = val
                            break
                    if(depth == 1):
                        alpha = max(l)[0]
                
                
                
                
                if(v != math.inf):
                    if depth == 1:
                        try:
                            return max(l)[1]
                        except(TypeError):
                            return l[0][1]
                    else:
                        return v , alpha, beta
            except(AttributeError):
                pass












