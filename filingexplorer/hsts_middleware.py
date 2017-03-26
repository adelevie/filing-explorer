class HSTSMiddleware:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        response = self.response(request)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        return response
