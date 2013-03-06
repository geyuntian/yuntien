from django.http import HttpResponse

class HttpResponseDirectOutput(HttpResponse):
    pass

class HttpResponseRichOutput(HttpResponse):
    _rich_title = ''
    _rich_head = ''
    _rich_sidebar = ''

    def get_title(self):
        return self._rich_title

    def set_title(self, title):
        self._rich_title = title
        
    def get_head(self):
        return self._rich_head

    def set_head(self, head):
        self._rich_head = head

    def get_sidebar(self):
        return self._rich_sidebar

    def set_sidebar(self, sidebar):
        self._rich_sidebar = sidebar
