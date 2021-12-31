from rest_framework.response import Response

SUCCESS_CODE = 'success'
ERROR_CODE = 'error'

def CodeResponse(code, **data):
    return Response({
        'code': code,
        'data': data
    }, content_type='application/json')

class CommonResponse:
    no_permission =  Response({
        'code': ERROR_CODE,
        'data': {
            'msg': 'NoPermission'
        }
    }, status=422, content_type='application/json')

    no_auth = Response({
        'code': ERROR_CODE,
        'data': {
            'msg': 'NoAuth'
        }
    }, status=401, content_type='application/json')

