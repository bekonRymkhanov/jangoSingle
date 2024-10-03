from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(max_length=255)
    profile_picture=models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user}s profile with bio: {self.bio} with picture  {self.profile_picture}"

    class Meta:
        db_table = "profile"


class Follow(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')  

    def __str__(self):
        return f"{self.follower} follows {self.following}"