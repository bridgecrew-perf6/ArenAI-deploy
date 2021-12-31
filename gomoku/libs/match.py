from .gomoku import ChessColor, GomokuGame, GameState
from .bot import ManualBot

class UnvalidMoveError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GomokuMatch:
    def __init__(self, black_bot, white_bot) -> None:
        self.game = GomokuGame()
        self.black_bot = black_bot
        self.white_bot = white_bot

    def check_move(self, move):
        if not isinstance(move, tuple): return False
        if len(move) != 2: return False
        if not (isinstance(move[0], int) and isinstance(move[1], int)): return False
        if not (0 <= move[0] <= 14 and 0 <= move[1] <= 14): return False
        return True
    
    async def run(self):
        while self.game.state in (GameState.BLACK_GOING, GameState.WHITE_GOING):
            bot = self.black_bot if self.game.state == GameState.BLACK_GOING else self.white_bot
            color = ChessColor.BLACK if self.game.state == GameState.BLACK_GOING else ChessColor.WHITE
            if isinstance(bot, ManualBot):
                print('wating for move')
                move = await bot.move()
            else:
                move = bot.move(self.game.board)
            if not self.check_move(move): raise UnvalidMoveError
            self.game.move(move[0], move[1])
            yield self.game.board, move, color
        
    


    