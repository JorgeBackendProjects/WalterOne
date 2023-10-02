''' The set of constants in walterone. '''
from enum import Enum

class Action(Enum):
    '''Actions a player can take'''
    Stop = 0
    Attack = 1
    Defend = 2
    Move = 3

class Role(str, Enum):
    ''' Roles assigned to a player '''
    BergenToy = 'BergenToy'
    Player = 'Player'