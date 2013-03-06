TYPE_TOP = 'top'
TYPE_SIDE = 'side'
TYPE_BOTTOM = 'bottom'
TYPE_POST_BOTTOM = 'post_bottom'

def plugin(request, config=[], types=[]):
    context = {}
    context['plugins'] = {}
    
    for type in types:
        plugins = [plugin for plugin in config if plugin['type'] == type]
        context['plugins'][type] = get_plugins_context(request, plugins)
    
    return context

def get_plugins_context(request, plugins):
    context = []
    for plugin in plugins:
        if plugin.has_key('view'):
            sections = plugin['view'].split('.')
            module = __import__('.'.join(sections[:-1]), globals(), locals(), sections[-1:], -1)
            view = getattr(module, sections[-1])
            plugin['data'] = view(request, render=lambda r,c:c)
        context.append(plugin)
    
    return context  
