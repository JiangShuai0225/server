from django.http import JsonResponse
import orjson

class PostMiddleware(object):
  def __init__(self, get_response):
    self.get_response = get_response
  def __call__(self, request):
    if request.method == 'POST':
      try:
        data = orjson.loads(request.body)
        # print(f'DATA:\t\t{data}')
        request.data = data
      except Exception as e:
        pass
      return self.get_response(request)
    else:
      return JsonResponse({ 'status': False, 'message': 'Method not allowed', 'data': {} })