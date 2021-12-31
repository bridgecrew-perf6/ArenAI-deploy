import json
import re
import time, asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from gomoku.libs.gomoku import GameState
from .libs.gomoku import ChessColor, GomokuGame, GameState
from .libs.bot import BotTemplate
from games.match import MATCHES
from games.bot import ManualBot
from copy import deepcopy


class GameMode:
    MANUAL = 1
    AUTO = 2

class UnvalidMoveError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GomokuConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.matchid = None
        await self.accept()

    async def handle_start_receive(self, content):
        if self.matchid in MATCHES:
            MATCHES.pop(self.matchid)
        matchid = content['data']['matchid']
        match = MATCHES[matchid]
        self.matchid = matchid
        self.black_bot = match['bots'][0]
        self.white_bot = match['bots'][1]

        assert not (isinstance(self.black_bot, ManualBot) and isinstance(self.white_bot, ManualBot))

        if isinstance(self.black_bot, ManualBot) or isinstance(self.white_bot, ManualBot):
            self.mode = GameMode.MANUAL
        else:
            self.mode = GameMode.AUTO
        
        self.game = GomokuGame()

        if self.mode == GameMode.AUTO:
            await self.start_auto_game()
        elif self.mode == GameMode.MANUAL:
            if isinstance(self.black_bot, ManualBot):
                self.manual_bot = self.black_bot
                self.auto_bot = self.white_bot
            else:
                self.manual_bot = self.white_bot
                self.auto_bot = self.black_bot
            
            if self.auto_bot.color == self.game.current_color:
                await self.auto_move(self.auto_bot)

    async def disconnect(self, code):
        MATCHES.pop(self.matchid)
        pass

    async def handle_move_receive(self, content):
        if self.mode == GameMode.MANUAL and \
            self.game.current_color == self.manual_bot.color and \
                self.game.state in (GameState.WHITE_GOING, GameState.BLACK_GOING):
            x = content['data']['x']
            y = content['data']['y']
            self.game.move(x, y)
            await self.send_move(x, y, self.manual_bot.color)
            if self.game.state in (GameState.BLACK_GOING, GameState.WHITE_GOING):
                await self.auto_move(self.auto_bot)
            else:
                print(self.game.state)

    

    async def receive_json(self, content, **kwargs):
        if 'action' in content:
            if content['action'] == 'move':
                await self.handle_move_receive(content)
            elif content['action'] == 'start':
                await self.handle_start_receive(content)
            elif content['action'] == 'end':
                if self.matchid in MATCHES:
                    MATCHES.pop(self.matchid)

    async def str_board(self, board):
        return [[it.name for it in row] for row in board]

    async def send_move(self, x, y, color):
        await self.send_json({
            'action': 'move',
            'data': {
                'move': {
                    'x': x,
                    'y': y
                },
                'color': color.name.lower()
            }
        })
        if not self.game.state in (GameState.BLACK_GOING, GameState.WHITE_GOING):
            await self.end_game()

    def check_move(self, move):
        if not isinstance(move, tuple): return False
        if len(move) != 2: return False
        if not (isinstance(move[0], int) and isinstance(move[1], int)): return False
        if not (0 <= move[0] <= 14 and 0 <= move[1] <= 14): return False
        return True

    async def auto_move(self, bot):
        assert not isinstance(bot, ManualBot)
        try:
            move = bot.move(deepcopy(self.game.board))
        except Exception as e:
            print(e)
            await self.send_json({
                'action': 'error',
                'data': {
                    'player': 'black' if bot is self.black_bot else 'white',
                    'exception': 'unknown'
                }
            })
            self.game.exception()
            return
        try:
            if not self.check_move(move): 
                raise UnvalidMoveError
            self.game.move(move[0], move[1])
            await self.send_move(move[0], move[1], bot.color)
        except Exception as e:
            await self.send_json({
                'action': 'error',
                'data': {
                    'player': 'black' if bot is self.black_bot else 'white',
                    'exception': 'UnvalidMove'
                }
            })
            self.game.exception()
        

    async def start_auto_game(self):
        while self.game.state in (GameState.BLACK_GOING, GameState.WHITE_GOING):
            bot = self.black_bot if self.game.state == GameState.BLACK_GOING else self.white_bot
            await self.auto_move(bot)
            await asyncio.sleep(0.1)

    async def end_game(self):
        assert self.game.state in (GameState.BLACK_WIN, GameState.WHITE_WIN, GameState.DRAW)
        await self.send_json({
            'action': 'end',
            'data': {
                'winner': 'black' if self.game.state == GameState.BLACK_WIN
                    else  'white' if self.game.state == GameState.WHITE_WIN
                    else  'draw'
            }
        })

    