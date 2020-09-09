from django.db import models
from django.utils import timezone

# Create your models here.
class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    images = models.ImageField(upload_to='')
    good = models.IntegerField(null=True, blank=True, default=0)
    read = models.IntegerField(null=True, blank=True, default=0)
    readtext = models.CharField(max_length=200, null=True, blank=True, default='a')
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BoardModel, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.text

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.text


