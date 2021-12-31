from rest_framework.views import APIView
from rest_framework.response import Response
from botenv.models import BotItem
from games.bot import ManualBot
from games.match import MATCHES
from games.models import Submission

from ArenAI.response import ERROR_CODE, SUCCESS_CODE, CodeResponse, CommonResponse

from ArenAI.settings import BOT_ENV_DIR, BOT_WORKSPACE_DIR

import sys, os
import time
import datetime


def get_timestamp():
    timestamp=time.time()
    time_local = time.localtime(timestamp)
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y%m%d%H%M%S%f")


from gomoku.consumers import ChessColor
BOT_PARAMS = {
    'gomoku': [{'color': ChessColor.BLACK}, {'color': ChessColor.WHITE}],
}


def restore_modules(save_modules):
    for mod in list(sys.modules.keys()):
        if not mod in save_modules:
            del sys.modules[mod]


class MatchView(APIView):
    
    def post(self, request, format=None):
        receive = request.data
        subids = receive['subids']

        sub_items = [Submission.objects.get(id=id) if (isinstance(id, str) and id != 'manual') else id for id in subids]
        game_name = sub_items[1].game_name if isinstance(sub_items[1], Submission) else sub_items[0].game_name
        save_modules = set(sys.modules.keys())
        bot_objs = []
        for playerID, (sub_item, init_params) in enumerate(zip(sub_items, BOT_PARAMS[game_name])):
            if sub_item == 'manual':
                bot_objs.append(ManualBot(**init_params))
            else:
                if isinstance(sub_item, dict):
                    bot = BotItem.objects.get(id=sub_item['botid'])
                    bot_info = {
                        'botid': bot.id,
                        'bot_path': bot.path,
                        'env_path': bot.env.path,
                        'exec_path': sub_item['execPath']
                    }
                else:
                    bot_info = {
                        'botid': sub_item.bot.id,
                        'bot_path': sub_item.bot.path,
                        'env_path': sub_item.bot.env.path,
                        'exec_path': sub_item.exec_path
                    }
                
                bot_exec_path = os.path.dirname(os.path.join(BOT_WORKSPACE_DIR, bot_info['bot_path'], bot_info['exec_path']))
                env_path = os.path.join(BOT_ENV_DIR, bot_info['env_path'])
                temp_path = sys.path
                try:
                    # sys.path = []
                    sys.path.append(bot_exec_path)
                    sys.path.append(os.path.join(env_path, 'Lib/site-packages'))
                    bot_objs.append(getattr(__import__(os.path.basename(bot_info['exec_path'])[:-len('.py')]), 'Bot')(**init_params))
                    sys.path.pop()
                    sys.path.pop()
                    sys.path = temp_path
                except Exception as e:
                    sys.path = temp_path
                    print(e)
                    restore_modules(save_modules)
                    return CodeResponse(ERROR_CODE, player = playerID + 1, exception = 'construction')
                finally:
                    restore_modules(save_modules)
        
        match_id = get_timestamp()
        MATCHES[match_id] = {
            'id': match_id,
            'bots': bot_objs
        }


        return CodeResponse(SUCCESS_CODE, matchid = match_id)


class SubmissonView(APIView):
    def get(self, request, format=None):
        receive = request.GET
        game_name = receive['gameName']
        return Response(
            {
                'action': 'listSubmission',
                'data': {
                    'submissions': [{
                        'id': s.id,
                        'user': s.bot.env.user.username,
                        'score': s.score,
                        'gameName': s.game_name,
                        'envName': s.bot.env.name.split('_')[-1],
                        'botName': s.bot.name.split('_')[-1]
                    } for s in Submission.objects.filter(game_name=game_name)]
                }
            }
        )
    
    def post(self, request, format=None):
        receive = request.data  
        botid = receive['botid']
        bot = BotItem.objects.get(id=botid)
        exec_path = receive['execPath']
        game_name = receive['gameName']
        if len(Submission.objects.filter(bot = bot, game_name=game_name)) > 0:
            submit = Submission.objects.filter(bot = bot, game_name=game_name)
            submit.update(exec_path = exec_path)
            return Response({
                'action': 'submit',
                'data': {
                    'msg': 'updated'
                }
            })
        
        submit = Submission.objects.create(bot=bot, game_name=game_name, exec_path=exec_path)
        submit.save()
        return Response({
            'action': 'submit',
            'data': {
                'msg': 'created'
            }
        })