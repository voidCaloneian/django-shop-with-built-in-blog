import time

class FakeLatencyMiddleware:
    "Установка исскуственной задержки между запросами"
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time.sleep(0.0) #  Сама задержка 
        response = self.get_response(request)
        return response