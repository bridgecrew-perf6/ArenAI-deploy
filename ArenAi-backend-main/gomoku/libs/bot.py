import asyncio


class BotTemplate:
    def __init__(self, color):
        self.color = color

    def move(self, board):
        raise NotImplementedError

# class ManualBot(BotTemplate):
#     pass