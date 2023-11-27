from django.test import TestCase
from django.contrib.auth import get_user_model
from blog_api_app.models import User, Post, Comment

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Create a post for testing
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test post content.'
        )

        # Create a comment for testing
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            comment='This is a test comment.'
        )

    def test_user_model(self):
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(str(user), 'testuser@example.com')

    def test_post_model(self):
        post = Post.objects.get(title='Test Post')
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post content.')
        self.assertEqual(str(post), 'testuser - Test Post')

    def test_comment_model(self):
        comment = Comment.objects.get(comment='This is a test comment.')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.comment, 'This is a test comment.')
        self.assertEqual(str(comment), 'testuser - Test Post')


'''
Result:

python manage.py test blog_api_app.tests.test_models
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 6.356s

OK
Destroying test database for alias 'default'...
'''