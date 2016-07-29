import numpy as np

from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax

#Андрей Ультра Про Прогер написал это

COLORS = {1, 2, 3 ,4}

def one_neib(neighbors):
    return any(n != 0 for n in neighbors)

def have_one_color(neighbors):
    return set(neighbors) != COLORS


#Переработка ввода в наш формат
def proces_input(inp):
    words = inp.split()
    return [(int(words[0]), int(words[1])), int(words[2])]

class GameOfColors( TwoPlayersGame ):
    """ In turn, the players remove one, two or three bones from a
    pile of bones. The player who removes the last bone loses. """

    def __init__(self, players, shape=(4, 4)):
        self.players = players
        self.nplayer = 1 # player 1 starts
        self.shape = shape
        self.first_move = True
        self.map_generate(shape)

    def map_generate(self, shape):
        self.map = np.zeros((self.shape[0]+2, self.shape[1]+2))
        for i in range(self.shape[0]+2):
            self.map[(i, 0)] = list(COLORS)[0]
            self.map[(i, self.shape[1]+1)] = list(COLORS)[1]
        for j in range(self.shape[1]+2):
            self.map[(0, j)] = list(COLORS)[2]
            self.map[(self.shape[0]+1, j)] = list(COLORS)[3]

    def generate_first_points(self):
        p1 = [' '.join([str(i), str(j), str(c)]) 
                                        for c in COLORS for i in  range(1, self.shape[0]+1) for j in [1, self.shape[1]]]
        p2 = [' '.join([str(i), str(j), str(c)]) 
                                        for c in COLORS for i in  [1, self.shape[0]] for j in range(1, self.shape[1]+1)]
        return p1 + p2

    def is_inside(self, point):
        return all(x in range(1, self.shape[i]+1) for i, x in enumerate(point))

    def find_neighbors(self, position):
        x, y = position
        return [(i, j) for i in range(x - 1, x + 2) 
            for j in range(y - 1, y + 2) 
                if [i, j] != [x, y] and self.is_inside((i, j))]
        

    def possible_moves(self):
        if self.first_move:
            points = self.generate_first_points()
            self.first_move = False
        else:
            points = []
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    neibs = self.find_neighbors((i, j))
                    if self.map[(i, j)] == 0 and one_neib(neibs) and have_one_color(neibs):
                       points += [' '.join([str(i), str(j), str(c)]) for c in COLORS - set(neibs)]
        return points

                
    def make_move(self,move):
        m = proces_input(move)
        self.map[m[0]] = m[1] # remove bones.

    def win(self):
        all(self.find_neighbors((i, j)) == COLORS for i in range(self.shape[0]) for j in range(self.shape[1]))

    def is_over(self): return self.win() # Game stops when someone wins.

    def show(self): print self.map
    
    def scoring(self): return 100 if self.win() else 0 # For the AI

# Start a match (and store the history of moves when it ends)

ai = Negamax(4) # The AI will think 13 moves in advance
game = GameOfColors([Human_Player(), AI_Player(ai)])
history = game.play()
