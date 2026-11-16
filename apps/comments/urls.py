from django.urls import path
from apps.comments.views import CreateCommentView

app_name = 'comments'

urlpatterns = [
    path('article/<int:article_id>/comment/', CreateCommentView.as_view(), name='create'),
]
