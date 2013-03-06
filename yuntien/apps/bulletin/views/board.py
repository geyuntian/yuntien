from django.shortcuts import *
from yuntien.community.main.models.community import Community, Widget

def show(request, render, community='', widget=''):
    w = Community.objects.get(key_name=community).widget_set.get(key_name=widget)
#    w = Widget.objects.filter(community=community).filter(key_name=widget)[0]
    if w:
        context = {'widget_config':w}
        return render(request, context)
    
    return HttpResponse('')
