from django.core.checks.messages import ERROR
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
import re
from django.core.cache import cache
# Create your views here.

from ArenAI.request import require_user
from ArenAI.response import CodeResponse, CommonResponse, ERROR_CODE, SUCCESS_CODE

USER_NAME_PATTERN = re.compile(r'[a-zA-Z][a-zA-Z0-9]+$')
PASSWORD_PATTERN = re.compile(r'[a-zA-Z0-9_\.]{6,32}$')

class TokenView(APIView):

    def post(self, request, format=None):
        receive = request.data
        username = receive.get('username')
        password = receive.get('password')
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return CodeResponse(ERROR_CODE, msg='UserDoesNotExist')

        user = auth.authenticate(username = username, password = password)
        if not user:
            return CodeResponse(ERROR_CODE, msg='WrongPassword')
        
        old_token = Token.objects.filter(user = user)
        old_token.delete()

        token = Token.objects.create(user = user)

        return CodeResponse(SUCCESS_CODE, token=token.key)

    @require_user
    def delete(self, request, format=None):
        cache.delete('token_' + request.user.auth_token.key)
        request.user.auth_token.delete()
        return CodeResponse(SUCCESS_CODE, msg="LoggedOut")
        


class UserView(APIView):

    @require_user
    def get(self, request, format=None):
        return CodeResponse(SUCCESS_CODE, username = request.user.username)
    
    def post(self, request, format=None):
        receive = request.data  
        username = receive['username']
        password = receive['password']
        
        if USER_NAME_PATTERN.match(username) is None:
            return CodeResponse(ERROR_CODE, msg='UnvalidUserName')
        if PASSWORD_PATTERN.match(password) is None:
            return CodeResponse(ERROR_CODE, msg='UnvalidPassword')

        try:
            User.objects.get(username=username)
            return CodeResponse(ERROR_CODE, msg='UserExist')
        except User.DoesNotExist:
            pass

        User.objects.create_user(username = username, password = password)
        return CodeResponse(SUCCESS_CODE, msg='UserCreated')
