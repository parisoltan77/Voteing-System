from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    title = models.CharField(max_length=50, unique=True)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null = True)
    bio = models.CharField(max_length = 300,null = True)
    resume = models.CharField(max_length = 50,null = True)
    total_vote = models.IntegerField(default=0, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    profile_pic = models.ImageField(verbose_name="Candidate Pic", upload_to='images/',null = True)

    def __str__(self):
        return "{}".format(self.position.title)


class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.position, self.status)
