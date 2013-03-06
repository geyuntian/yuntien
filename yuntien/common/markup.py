from postmarkup import render_bbcode

class TextMarkup(object):
    
    def render(self, text):
        return

class PostMarkup(TextMarkup):
    
    def render(self, text):
        return render_bbcode( text )

text_markup = PostMarkup()
