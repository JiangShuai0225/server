import time

class TimeShowMiddleware(object):
  def __init__(self, get_response):
    self.get_response = get_response
  def __call__(self, request):
    print("=" * 50)
    print(f'URL: \t\t{request.path}')
    print(f'METHOD: \t{request.method}')
    time_start = time.time()
    response = self.get_response(request)
    time_end = time.time()
    print(f'TIME: \t\t{(time_end - time_start) * 1000:.6f} ms')
    return response