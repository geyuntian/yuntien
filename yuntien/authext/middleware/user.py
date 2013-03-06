from yuntien.authext.models.user import set_current_user

class InitMiddleware(object):
    def process_request(self, request):
        set_current_user(request.user)
        return None
