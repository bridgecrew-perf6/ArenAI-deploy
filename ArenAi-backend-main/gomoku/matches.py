from .libs.match import GomokuMatch
from .libs.bot import BotTemplate
class Bot(BotTemplate):
    def move(self, board):
        for x in range(15):
            for y in range(15):
                if board[x][y].name == 'EMPTY':
                    return (x, y)
    

matches = dict()

