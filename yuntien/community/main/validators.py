from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from yuntien.community.main.models.community import Community

def validate_community(value):
    try:
        Community.objects.get(key_name=value)
    except:
        raise ValidationError(_(u'%s is not a valid community.') % value)
