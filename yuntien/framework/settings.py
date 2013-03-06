# -*- coding:utf-8 -*-
from django.conf import settings

CONTAINER_ID_REGEX = r'[a-z][a-z0-9-]{1,29}'
AREA_ID_REGEX = CONTAINER_ID_REGEX
WIDGET_ID_REGEX = CONTAINER_ID_REGEX

SOURCE_TYPE_DEFAULT = 1
SOURCE_TYPE_USER = 2
SOURCE_TYPE_COMMUNITY = 3

SOURCE = {

SOURCE_TYPE_DEFAULT : {
'source': {
'app_label': 'user',
'model': 'userprofile'
},
},

SOURCE_TYPE_USER : {
'source': {
'app_label': 'user',
'model': 'userprofile'
},
'source_widget': {
'app_label': 'user',
'model': 'widget'
},
},

SOURCE_TYPE_COMMUNITY : {
'source': {
'app_label': 'main',
'model': 'community'
},
'source_widget': {
'app_label': 'main',
'model': 'widget'
},
}

}