from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models import Category, Article
from apps.comments.services import CommentService


class CommentServiceTests(TestCase):
    def setUp(self):
        self.comment_service = CommentService()
        self.user = User.objects.create_user(username='srv_commenter', password='pwd')
        self.category = Category.objects.create(name='علم', slug='science')
        self.article = Article.objects.create(
            title='فیزیک کوانتوم',
            slug='quantum-physics',
            summary='خلاصه کوانتوم',
            content='محتوای کوانتوم',
            category=self.category,
            author=self.user
        )

    def test_add_comment(self):
        comment = self.comment_service.add_comment(
            article=self.article,
            author=self.user,
            content='دیدگاهی درباره کوانتوم'
        )
        self.assertEqual(comment.content, 'دیدگاهی درباره کوانتوم')

        approved = self.comment_service.get_approved_comments_for_article(self.article.pk)
        self.assertEqual(approved.count(), 1)
