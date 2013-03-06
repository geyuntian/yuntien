import re
import urllib2

youku_url = re.compile(u"^http://v.youku.com/v_show/id_(.*).html$")
youku_url2 = re.compile(u"^http://player.youku.com/player.php/sid/(.*)/v.swf$")
tudou_url = re.compile(u"^http://www.tudou.com/programs/view/(.*)/?$")
tudou_url2 = re.compile(u"^http://www.tudou.com/v/(.*)$")
ku6_url = re.compile(u"^http://v.ku6.com/show/(.*).html$")
ku6_url2 = re.compile(u"^http://player.ku6.com/refer/(.*)/v.swf$")

def transform_video_url(url):
    if not url:
        return (False, url)
    
    m = tudou_url.match(url) 
    if m:
        return (True, u"http://www.tudou.com/v/%s" % m.group(1))

    m = tudou_url2.match(url) 
    if m:
        return (True, url)
        
    m = youku_url.match(url) 
    if m:
        return (True, u"http://player.youku.com/player.php/sid/%s/v.swf" % m.group(1))

    m = youku_url2.match(url) 
    if m:
        return (True, url)

    m = ku6_url.match(url) 
    if m:
        return (True, u"http://player.ku6.com/refer/%s/v.swf" % m.group(1))

    m = ku6_url2.match(url) 
    if m:
        return (True, url)
    
    return (False, url)

def get_domain(url):
    str_table = url.split('/')
    for str in str_table[1:]:
        if str:
            return str

class HeadRequest(urllib2.Request):
     def get_method(self):
         return "HEAD"

def get_headers(url):
    try:
        return urllib2.urlopen(HeadRequest(url)).headers.dict
    except:
        pass    

def is_valid_image_url(url):
    headers = get_headers(url)
    if headers and 'content-type' in headers and 'image/' in headers['content-type']:
        return True
    else:
        return False
