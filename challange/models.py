from django.db import models


# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    personalCode = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    verifcode = models.IntegerField()


class Question(models.Model):
    text = models.CharField(max_length=255)
    cases = models.CharField(max_length=255)
    answer = models.CharField(max_length=100)
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start = models.TimeField(auto_now=False, auto_now_add=False)
    end = models.TimeField(auto_now=False, auto_now_add=False)
    minpoint = models.IntegerField()

# class Log(models.Model):

#     member = models.ForeignKey("Member")
#     logtime = models.TimeField(auto_now=False, auto_now_add=True)
