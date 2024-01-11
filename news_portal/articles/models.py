from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] * 3
        comments_rating = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum']
        self_posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        self.rating = posts_rating + comments_rating + (self_posts_comments_rating or 0)
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    creation_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return Truncator(self.text).chars(124) + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
