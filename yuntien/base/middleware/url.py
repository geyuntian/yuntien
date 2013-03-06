class URLMiddleware(object):
    """
    This is a very simple middleware that add google account user to request
    """
    def process_request(self, request):
        try:
            url = 'http'
            if request.is_secure():
                url += 's'
            url += '://'
            url += request.META['HTTP_HOST']
            request.host_url = url
        except:
            request.host_url = ''