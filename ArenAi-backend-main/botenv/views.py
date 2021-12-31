from rest_framework.views import APIView
from rest_framework.response import Response

from .models import BotEnv, BotItem
from ArenAI.settings import BOT_ENV_DIR, BOT_WORKSPACE_DIR, TEMP_DIR
import os
import venv
from pip._internal.metadata import get_environment
from pip import main as pip_main
from ArenAI.response import SUCCESS_CODE, CodeResponse
from django.http import StreamingHttpResponse
import shutil
import zipfile

# Create your views here.

def get_env_packages(env_name):
    env = get_environment([os.path.join(BOT_ENV_DIR, env_name, 'Lib/site-packages')])
    packages = [{
        'name': d.raw_name,
        'version': d.version.base_version
    } for d in env.iter_installed_distributions() ]
    return packages



class BotEnvView(APIView):

    def put(self, request, format = None):
        receive = request.data
        user = request.user
        envid = receive['envid']
        packages = receive['packages']
        

        if len(BotEnv.objects.filter(user=user, id=envid)) == 0:
            return Response(status=412)
        
        env = BotEnv.objects.get(id=envid)
        env_name = env.name
        pack_list = get_env_packages(env_name)

        pack_dict = {
            item['name']: item['version']
        for item in pack_list}

        new_pack_dict = {
            item['name']: item['version']
        for item in packages}

        target_dir = os.path.join(BOT_ENV_DIR, env.path, 'Lib/site-packages')

        for name, version in new_pack_dict.items():
            pack_name = name if version == '' else f'{name}=={version}'
            if not name in pack_dict:
                pip_main(['install', pack_name, f'--target={target_dir}'])
            elif pack_dict[name] != version and version != '':
                pip_main(['install', pack_name, f'--target={target_dir}'])
        
        for name, version in pack_dict.items():
            if not name in new_pack_dict:
                pip_main(['uninstall', name])

        return Response({
            'action': 'updatePackages',
            'data': {
                'msg': 'All updated'
            }
        })


    def get(self, request, format = None):
        receive = request.GET
        user = request.user
        envid = receive['envid']
        if len(BotEnv.objects.filter(user=user, id=envid)) == 0:
            return Response(status=412)
        env = BotEnv.objects.get(id=envid)
        env_name = env.name
        pack_list = get_env_packages(env_name)
        return Response(pack_list)

    def post(self, request, format=None):
        receive = request.data
        user = request.user
        env_name = receive['name']
        env_name = f'{user.id}_{env_name}'
        if len(BotEnv.objects.filter(name = env_name)) > 0:
            return Response(status=412)

        env_dir = os.path.join(BOT_ENV_DIR, env_name)
        os.makedirs(env_dir)
        env_creator = venv.EnvBuilder()
        env_creator.create(env_dir)
        env = BotEnv.objects.create(user=user, name=env_name, path=env_name)
        env.save()
        return Response({
            'action': 'info',
            'data': {
                'msg': f'Env {env_name} for user {user.username} created'
            }
        })

class BotAllView(APIView):
    def get(self, request, format=None):
        uid = request.user.id
        env_prefix = f'{uid}_'
        envs = []
        for e in BotEnv.objects.filter(user=request.user):
            bots = []
            for bot in BotItem.objects.filter(env = e):
                bot_prefix = f'{env_prefix}_{e.id}'
                bots.append({
                    'name': bot.name[len(bot_prefix):],
                    'id': bot.id
                })

            envs.append({
                'name': e.name[len(env_prefix):],
                'id': e.id,
                'bots': bots
            })

        return Response(envs)

def listdirtree(path, root_path=None, ret=None, format_filter=None):
    if ret is None:
        ret = []
    for i in os.listdir(path):
        if i == '__pycache__': continue
        path2 = os.path.join(path,i) 
        if os.path.isdir(path2):
            listdirtree(path2, root_path, ret, format_filter)
        else:
            if format_filter is None or i[-len(format_filter) -1 :] == f'.{format_filter}':
                if root_path is None:
                    ret.append(path2)
                else:
                    ret.append(os.path.relpath(path2, root_path))
                
    return ret

class BotDownloadView(APIView):
    def get(self, request, format=None):
        receive = request.GET
        botid = int(receive['botid'])
        bot = BotItem.objects.get(id = botid)
        folder_path = os.path.join(BOT_WORKSPACE_DIR, bot.path)
        file_list = listdirtree(folder_path)
        print(file_list)
        botfile_path = os.path.join(TEMP_DIR, bot.name) + '.zip'
        botfile = zipfile.ZipFile(botfile_path, 'w')
        for file in file_list:
            botfile.write(file, arcname=os.path.relpath(file, folder_path))
        botfile.close()
        file = open(botfile_path, 'rb')
        response = StreamingHttpResponse(file, headers={
            'content-type': 'application/zip',
            'content-disposition': f'''{bot.name.split('_')[-1] + '.zip'}''',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        })
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = f'''attachment;filename="{bot.name.split('_')[-1] + '.zip'}"'''
        return response





class BotItemView(APIView):

    def get(self, request, format=None):
        receive = request.GET
        botid = int(receive['botid'])
        bot = BotItem.objects.get(id = botid)
        folder_path = os.path.join(BOT_WORKSPACE_DIR, bot.path)
        file_list = listdirtree(folder_path, folder_path, format_filter='py')
        return Response({
            'action': 'getBotFileList',
            'data': {
                'fileList': file_list
            }
        })
        

    def post(self, request, format=None):
        receive = request.data  
        user = request.user
        envid = receive['envid']
        bot_name = receive['name']
        bot_name = f'{user.id}_{envid}_{bot_name}'
        if len(BotEnv.objects.filter(user=user, id=envid)) == 0:
            return Response(status=412)
        if len(BotItem.objects.filter(name=bot_name)) > 0:
            return Response(status=412)

        env = BotEnv.objects.get(id=envid)

        os.makedirs(os.path.join(BOT_WORKSPACE_DIR, bot_name))
        bot = BotItem.objects.create(env=env, name=bot_name, path=bot_name)
        bot.save()

        return Response({
            'action': 'info',
            'data': {
                'msg': f'Bot {bot_name} in Env {env.name} for user {user.username} created'
            }
        })

    def delete(self, request, format=None):
        receive = request.data
        botid = receive['botid']
        

    def put(self, request, format=None):
        receive = request.data
        botid = receive['botid']
        got_path = receive.getlist('relativePath')
        files = request.FILES.getlist('files')
        
        # no error handling
        
        bot = BotItem.objects.get(id = botid)
        target_dir = os.path.join(BOT_WORKSPACE_DIR, bot.path)
        shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        for i, file_obj in enumerate(files):
            save_path = os.path.join(target_dir, got_path[i])
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as save_file:
                for chunk in file_obj.chunks():
                    save_file.write(chunk)

        return Response({
            'action': 'info',
            'data': {
                'msg': 'upload files successfully'
            }
        })


