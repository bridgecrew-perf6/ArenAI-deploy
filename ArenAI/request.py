from ArenAI.response import CommonResponse

def require_user(func):
    def check(self, request, format=None):
        if not 'Authorization' in request.headers:
            return CommonResponse.no_auth
        if request.user.is_authenticated:
            return func(self, request, format)
        else:
            return CommonResponse.no_auth
            
    return check