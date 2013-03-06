from django.core.urlresolvers import reverse, resolve
from yuntien.app import settings
from yuntien.status.models.status import SOURCE_TYPE_DEFAULT

def get_status_url(status):
    if status.source_type == SOURCE_TYPE_DEFAULT:
        kwargs = {'user': status.user.username, 'id':status.id}
        return reverse('user-statuses-show', kwargs=kwargs)
    
    try:
        urls = status.app.settings['urls']
        view, args, kwargs = resolve(settings.APP_API_STATUS_URL, urls)
        return view(None, status)
    except:
        kwargs = {'user': status.user.username, 'id':status.id}
        return reverse('user-statuses-show', kwargs=kwargs)

def render_status(context, status):
    app = None
    if status.is_repost == False:
        app = status.app
    elif status.re_status:
        app = status.re_status.app
        
    if app and app.render_status:
        try:
            urls = app.settings['urls']
            view, args, kwargs = resolve(settings.APP_API_STATUS_RENDER, urls)
            return view(context['request'], status).content
        except Exception as e:
            pass
