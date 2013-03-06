from yuntien.base.views.plugin import plugin as _plugin
from yuntien.base.views.plugin import *
from yuntien.user.settings import USER_WIDGETS

def apps(request):
    context = {}
    context['user_widgets'] = USER_WIDGETS
    context['user_widgets'] = [USER_WIDGETS[w] for w in sorted(USER_WIDGETS, key=lambda w: USER_WIDGETS[w]['sort'])]    
    return context
