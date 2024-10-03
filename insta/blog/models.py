from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} with {self.content} that created  {self.created_at} with author: {self.author}"



class Comment(models.Model):
    content=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.content} that created at {self.created_at} with post  {self.post} with author: {self.author}"
 




