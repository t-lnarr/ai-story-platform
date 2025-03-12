from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    title = models.CharField(max_length=200, default="Unnamed Story")
    genre = models.CharField(max_length=100, blank=True)
    max_contributors = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)  # Görsel alanı

    def __str__(self):
        return self.title

class Contribution(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="contributions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcı eklendi
    user_input = models.TextField(max_length=200)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.story.title} - {self.user_input[:20]} by {self.user.username}"

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcı eklendi
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.story.title} - {self.text[:20]} by {self.user.username}"

class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcı eklendi
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')  # Bir kullanıcı bir hikâyeye tek beğeni atabilir

    def __str__(self):
        return f"{self.story.title} - Like by {self.user.username}"
