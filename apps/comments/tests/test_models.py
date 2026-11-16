from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models import Category, Article
from apps.comments.models import Comment
from apps.comments.enums import CommentStatus


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='pwd')
        self.category = Category.objects.create(name='هنر', slug='art')
        self.article = Article.objects.create(
            title='هنر مدرن',
            slug='modern-art',
            summary='خلاصه',
            content='محتوا',
            category=self.category,
            author=self.user
        )

    def test_comment_creation_and_defaults(self):
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content='دیدگاه بسیار ارزشمند درباره هنر مدرن'
        )
        self.assertEqual(comment.status, CommentStatus.APPROVED)
        self.assertIn('commenter', str(comment))
        self.assertIsNone(comment.parent)
