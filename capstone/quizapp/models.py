from django.db import models
from django.contrib.auth.models import AbstractUser

  
# Create your models here.
CHOICES = {
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
}


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



class Quiz(models.Model):
    creator = models.CharField(max_length=64)
    name = models.CharField(max_length = 120)
    subject = models.CharField(max_length = 120)
    questionamt = models.IntegerField()
    time = models.IntegerField()
    passingscore = models.IntegerField()
    difficulty = models.CharField(max_length=6, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now=True)
    bestscoreuser = models.CharField(max_length=64, default=None)
    bestscore = models.IntegerField(default=None)

    def __str__(self):
        return f"{self.name}, {self.subject}"

    # limit to questionamt
    def getQuestions(self):
        return self.question_set.all()[:self.questionamt]

class Final(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.CharField(max_length = 120)
    score = models.FloatField()


    def __str__(self):
        return f"{self.user} got a score of {self.score}"


class Question(models.Model):
    body = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    timemade = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.body}"
    

    def getAnswer(self):
        return self.answer_set.all() 


class Answer(models.Model):
    body = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timemade = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"question: {self.question.body}, answer: {self.body}, correct: {self.correct}"




