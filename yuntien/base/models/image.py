from django.core.files.storage import default_storage
from django.core.files.base import File, ContentFile
from django.db import models

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import Image
except:
    pass

class ImageBaseHanlder(object):
    
    def process(self, file):
        pass
    
class ImageHandler(ImageBaseHanlder):
    
    def __init__(self, name):
        self.name = name
    
    def process(self, file):
        #save the file directly
        name = self.name
        if default_storage.exists(name):
            default_storage.delete(name)
        default_storage.save(name, file)
        
class SquareImageHandler(ImageBaseHanlder):

    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def process(self, file):
        try:
            im = Image.open(file)
            im_x, im_y = im.size
            
            if im_x >= im_y:
                box = ((im_x-im_y)/2, 0, (im_x-im_y)/2+im_y, im_y)
            else:
                box = (0, (im_y-im_x)/2, im_x, (im_y-im_x)/2+im_x)
            
            im = im.crop(box)
            size = self.size, self.size
            
            im_x_new, im_y_new = im.size
            if im_x_new > im_x:            
                im = im.resize(size, Image.ANTIALIAS)
            else:
                #thumbnail is faster
                im.thumbnail(size, Image.ANTIALIAS)
            
            output = StringIO()
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(output, "JPEG", quality=95)
            
            #save file
            if default_storage.exists(self.name):
                default_storage.delete(self.name)
            default_storage.save(self.name, ContentFile(output.getvalue()))        
            
            output.close()
        except IOError as e:
            pass
        
class FixedWidthImageHandler(ImageBaseHanlder):

    def __init__(self, name, width, max_height=None):
        self.name = name
        self.width = width
        self.max_height = max_height
    
    def process(self, file):
        try:
            im = Image.open(file)
            im_x, im_y = im.size
            
            x = self.width
            ratio = x * 1.0 / im_x
            y = int( im_y * ratio )
            
            if self.max_height and y > self.max_height:
                y = self.max_height
                ratio = y * 1.0 / im_y
                x = int( im_x * ratio)
            
            size = x, y
            
            if ratio > 1:
                im = im.resize(size, Image.ANTIALIAS)
            else:
                #thumbnail is faster
                im.thumbnail(size, Image.ANTIALIAS)           
            
            output = StringIO()
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(output, "JPEG", quality=95)
            
            #save file
            if default_storage.exists(self.name):
                default_storage.delete(self.name)
            default_storage.save(self.name, ContentFile(output.getvalue()))
            
            output.close()
        except IOError as e:
            pass

class ImageMixin(object):
    
    def save_image(self, file, handlers):
        for handler in handlers:
            file.seek(0)
            #sometimes the image will be modified in place,
            #so we copy the file to a ContentFile 
            content_file = ContentFile(file.read())
            handler.process(content_file)
