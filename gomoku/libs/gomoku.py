from enum import Enum

class ChessColor(Enum):
    BLACK = 1
    WHITE = 2
    EMPTY = 3

class GameState(Enum):
    BLACK_GOING = 1
    WHITE_GOING = 2
    BLACK_WIN = 3
    WHITE_WIN = 4
    DRAW = 5
    EXCEPTION = 6

class GomokuGame():
    def __init__(self):
        # 棋盘大小
        self._boardSize=15
        # 当前棋盘矩阵,board[i][j]，代表第i行第j列(从0算)
        self._board=[[ChessColor.EMPTY]*self._boardSize for _ in range(self._boardSize)]
        # 当前行动的人
        self._nowColor = ChessColor.BLACK
        self._state = GameState.BLACK_GOING
        self._chess_num = 0

    def exception(self):
        self._state = GameState.EXCEPTION

    def print_board(self):
        for i in range(self._boardSize):
            print(self._board[i])

    @property
    def current_color(self):
        return self._nowColor

    @property
    def state(self):
        return self._state

    @property
    def board(self):
        return self._board

    # 判断chess在pos位置是否可落子
    def is_valid_move(self, x, y, color):
        return (self._board[x][y] == ChessColor.EMPTY) and (color == self._nowColor)

    #某种棋子落在(x,y位置)，(1,1)为棋盘左上角落点。
    def move(self, x, y):
        color = ChessColor.BLACK if self.state == GameState.BLACK_GOING else ChessColor.WHITE
        assert self.is_valid_move(x, y, color), f'Unvalid move {x} {y} {color.name}'
        self._board[x][y] = color
        
        # Update game state
        if self._win(x,y):
            if self.state == GameState.BLACK_GOING:
                self._state =  GameState.BLACK_WIN
            elif self.state == GameState.WHITE_GOING:
                self._state = GameState.WHITE_WIN
        else:
            if self.state == GameState.BLACK_GOING:
                self._state = GameState.WHITE_GOING
            elif self.state == GameState.WHITE_GOING:
                self._state = GameState.BLACK_GOING
        
        #落子后，改变行动的角色
        self._nowColor = ChessColor.BLACK if self._nowColor == ChessColor.WHITE else ChessColor.WHITE
        
        self._chess_num += 1
        if self._chess_num == self._boardSize * self._boardSize:
            self._state = GameState.DRAW

    #当最新的落子为(x,y)时，判断游戏是否结束
    def _win(self,x,y):
        cur_value = self._board[x][y]
        for direction in ((1, 0), (0, 1), (1, 1), (1, -1)):
            if self._get_count_on_direction(x,y, cur_value, direction[0], direction[1]):
                return True
        return False

    #以(x,y)为值为value的初始点，判断偏移后新位置是否也是value,若是则count++，如果count>=5，游戏结束
    def _get_count_on_direction(self, X,Y, value, x_offset, y_offset):
        count = 1
        for step in range(1, 5):
            x = X + step * x_offset
            y = Y + step * y_offset
            if 0 <= x < self._boardSize and 0 <= y < self._boardSize and self._board[x][y] == value:
                count += 1
            else:
                break
        for step in range(1, 5):
            x = X - step * x_offset
            y = Y - step * y_offset
            if 0 <= x < self._boardSize and 0 <= y < self._boardSize and self._board[x][y] == value:
                count += 1
            else:
                break
        return count >= 5

# game=gobangGame()
# game.put_chess(0,5,1)
# game.print_board()
