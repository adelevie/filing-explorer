class HSTSMiddleware:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        response = self.response(request)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        return response

# from http://stackoverflow.com/questions/19991339/best-way-to-achive-the-opposite-of-prepend-www-e-g-redirect-from-www-to-root
class RemoveWwwMiddleware():
    def __call__(self, request):
        try:
            if request.META['HTTP_HOST'].lower().find('www.') == 0:
                from django.http import HttpResponsePermanentRedirect
                return HttpResponsePermanentRedirect(request.build_absolute_uri().replace('//www.', '//'))
        except:
            pass
