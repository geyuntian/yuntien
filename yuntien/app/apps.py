# -*- coding:utf-8 -*-
DEFAULT_APPS = {

'bulletin': {
'id':'bulletin',
'key_name':'bulletin',
'sort':5,
'name':u'公告',
'urls':'yuntien.apps.bulletin.app',
'style':'',
'stylesheet':'',
'multiple_widgets':True,
'has_app_page':False,
},

'tui': {
'id':'tui',
'key_name':'tui',
'sort':10,
'name':u'推荐',
'urls':'yuntien.apps.tui.app',
'style':'/static/style/community/tui-app.css',
'stylesheet':'/static/style/community/tui-app.css',
'multiple_widgets':False,
'has_app_page':True,
'render_status':True,
},

'forum': {
'id':'forum',
'key_name':'forum',
'sort':15,
'name':u'论坛',
'urls':'yuntien.apps.forum.app',
'style':'/static/style/community/forum-app.css',
'stylesheet':'/static/style/community/forum-app.css',
'multiple_widgets':True,
'has_app_page':True,
},

#'qa': {
#'id':'qa',
#'sort':20,
#'name':u'问答',
#'urls':'yuntien.apps.qa.app',
#'style':'/static/style/community/qa-app.css',
#'multiple_widgets':False,
#'has_app_page':False,
#},
#
#'poll': {
#'id':'poll',
#'sort':30,
#'name':u'投票',
#'urls':'yuntien.apps.poll.app',
#'style':'/static/style/community/poll-app.css',
#'multiple_widgets':False,
#'has_app_page':False,
#},

'note': {
'id':'note',
'key_name':'note',
'sort':40,
'name':u'记录',
'urls':'yuntien.apps.note.app',
'style':'/static/style/community/note-app.css',
'stylesheet':'/static/style/community/note-app.css',
'multiple_widgets':True,
'has_app_page':True,
},

'photos': {
'id':'photos',
'key_name':'photos',
'sort':30,
'name':u'相册',
'urls':'yuntien.apps.photos.app',
'style':'/static/style/community/note-app.css',
'stylesheet':'/static/style/community/note-app.css',
'multiple_widgets':True,
'has_app_page':False,
'render_status':True,
},

}
