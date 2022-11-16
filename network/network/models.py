from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    #Unfollow function that deletes user's follwing object from Follwer model
    def unfollow(self, username):
        Follower.objects.get(follower=self, following=username).delete()

    #Follow function that creates a following object in the Follower model
    def follow(self, username):
        Follower.objects.create(follower=self, following=username)


    pass


#Model for all follower/following relationships
class Follower(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
    class Meta:
        unique_together = ('following', 'follower')

#Model for posts
class Post(models.Model):  
    user = models.CharField(max_length=32)
    body = models.TextField(max_length=800)
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "likes": self.likes
        }


#Model to store likes
class Like(models.Model):
    body = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likedpost')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likeduser')

    class Meta:
        unique_together = ('body', 'user')

