import jwt
from django.http import JsonResponse
from django.conf import settings

class JwtVerifyMiddleware(object):
  def __init__(self, get_response):
    self.get_response = get_response
  def __call__(self, request):
    white_list = ['/api/login']
    if request.path in white_list:
      print('OK')
      return self.get_response(request)
    try:
      token = request.data.get('token')
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      # print(f'PAYLOAD:\t{payload}')
      request.payload = payload
      
      while_list = ['/api/login', '/api/ticket/create', '/api/ticket/check', '/api/ticket/decument',]
      if request.payload.get('status') == 3:
        if request.path in while_list:
          return self.get_response(request)
        else:
          return JsonResponse({ 'status': False, 'message': 'URL not allowed', 'data': {} })
      else:
        return self.get_response(request)
    except Exception as e:
      return JsonResponse({ 'status': False, 'message': 'Token Error', 'data': {} })
