#!/usr/bin/env python3

import math, random
from ...lib.game import discrete_soccer, connect_four

def soccer(state, player_id):
    # TODO: Implement this function!
    #
    # The soccer evaluation function *must* look into the game state
    # when running. It will then return a number, where the larger the
    # number, the better the expected reward (or lower bound reward)
    # will be.
    #
    # For a good evaluation function, you will need to
    # SoccerState-specific information. The file
    # `src/lib/game/discrete_soccer.py` provides a description of all
    # useful SoccerState properties.
    
    opponent_id = 0 if player_id == 1 else 1
    
    #ball possesion
    p_has_ball = state.players[player_id]['has_ball']
    o_has_ball = state.players[opponent_id]['has_ball']
    #team names
    p_team = state.players[player_id]['team']
    o_team = state.players[player_id]['team'].inverse
    #positions
    p_pos = (state.players[player_id]['x'],state.players[player_id]['y'])
    o_pos = (state.players[opponent_id]['x'],state.players[opponent_id]['y'])
    b_pos = (state.ball['x'],state.ball['y'])
    #distances to player goal
    p_pgoal_dist = state.dist_to_goal(p_pos,p_team)
    o_pgoal_dist = state.dist_to_goal(o_pos,p_team)
    #distances to opponent goal
    p_ogoal_dist = state.dist_to_goal(p_pos,o_team)
    o_ogoal_dist = state.dist_to_goal(o_pos,o_team)
    #distances to ball
    pb_dist = math.sqrt((p_pos[0]-b_pos[0])**2+(p_pos[1]-b_pos[1])**2)
    ob_dist = math.sqrt((o_pos[0]-b_pos[0])**2+(o_pos[1]-b_pos[1])**2)
    #distances to players
    po_dist = math.sqrt((p_pos[0]-o_pos[0])**2+(p_pos[1]-o_pos[1])**2)
    po_Xdist = p_pos[0]-o_pos[0]
    po_Ydist = p_pos[0]-o_pos[0]
    print("po_Xdist:",po_Xdist)
    print("po_Ydist:",po_Ydist)
    
    #########################################
    #if player scored goal
    if ((p_team.name == 'red' and state.ball_in_red_goal) or (p_team.name == 'blue' and state.ball_in_blue_goal)):
        return 10
    
    #if opponent scored goal
    if ((o_team.name == 'red' and state.ball_in_red_goal) or (o_team.name == 'blue' and state.ball_in_blue_goal)):
        return -10
    #########################################
    
    #########################################
    #if has ball and opponent is between goal and player +4
    if (p_has_ball and (o_pgoal_dist < p_pgoal_dist)):
        return 4 - translate(p_pgoal_dist) + translate(po_dist)
    
    #if has ball and opponent is behind player +7
    elif (p_has_ball and (o_pgoal_dist >= p_pgoal_dist)):
        return 7 - translate(p_pgoal_dist) + translate(po_dist)
    #########################################
    
    #########################################
    #if opponent has ball and player is between goal and opponent
    if (o_has_ball and (p_ogoal_dist < o_ogoal_dist)):
        if(p_pos[1] < state.goal_top and p_pos[1] > state.goal_bottom):
                if(p_pos[0] < state.blue_goal_pos[0] + 6 if p_team.name == 'blue' else state.red_goal_pos[0] - 6 and p_pos[0] > 0):  
                    if(state.can_shoot_from(o_pos[0],o_pos[1],o_team)):
                        return -3 - translate(po_dist)
                    else:
                        return -5 - translate(po_dist)
        return -4 - translate(po_dist) - translate(p_ogoal_dist + 2) 
    
    #if opponent has ball and player is behind opponent
    if (o_has_ball and (p_ogoal_dist >= o_ogoal_dist)):
        return -7 - translate(p_ogoal_dist) #- translate(po_dist)
    #########################################
    
    
    
    #########################################
    #if doesnt have ball and opponent doesnt have ball, but is closer 
    if (not p_has_ball and not o_has_ball and (pb_dist > ob_dist)):
        return 1 - translate(pb_dist) 
    
    #if doesnt have ball and opponent doesnt have ball, but is further 
    if (not p_has_ball and not o_has_ball and (pb_dist < ob_dist)):
        return -1 - translate(pb_dist)
    
    #if doesnt have ball and opponent doesnt have ball
    if (not p_has_ball and not o_has_ball):
        return 0 
    #########################################
    
    if not isinstance(state, discrete_soccer.SoccerState):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0

def connect_four(state, player_id):
    if not isinstance(state, connect_four.Connect4State):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0


def translate(value, leftMin = 0, leftMax = 100, rightMin = 0, rightMax = 0):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    #rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    return valueScaled
    # Convert the 0-1 range into a value in the right range.
    #return rightMin + (valueScaled * rightSpan)