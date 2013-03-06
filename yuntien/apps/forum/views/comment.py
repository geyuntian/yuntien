from django import forms
from yuntien.authext.views.decorators import check_authorization, OPERATION_ADD, OPERATION_DELETE
from yuntien.base.views.decorators.db import *
from yuntien.apps.forum.models import Topic, Comment
from yuntien.common.markup import text_markup

class CommentForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)

@check_authorization(Comment, OPERATION_ADD)
def add(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Topic.objects.get(pk=id)
            comment = Comment()
            comment.topic = post
            comment.author = request.user
            comment.content = text_markup.render( form.cleaned_data['content'] )
            comment.raw_content = form.cleaned_data['content']
            comment.community = post.community
            comment.community_widget = post.community_widget
            comment.save()
            post.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseNotFound()

@check_id(Comment)
@check_authorization(Comment, OPERATION_DELETE)
def delete(request, id):
    if request.method == 'POST':
        model = Comment.objects.get(pk=id)
        model.delete()
        return HttpResponse('Deleted!')
    return HttpResponseNotFound()
