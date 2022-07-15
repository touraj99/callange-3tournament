from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Member(AbstractUser):
    name = models.CharField(max_length=100)
    personalCode = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    verifcode = models.IntegerField(default=0)
    isadmin = models.BooleanField(default=False)


class Question(models.Model):
    STATUS_CHOICES = (
        ('s', 'single'),
        ('m', 'multi')
    )
    text = models.CharField(max_length=255)
    cases = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    order = models.IntegerField(default=1)
    type = models.CharField(max_length=1, choices=STATUS_CHOICES, default="s")
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField(auto_now=False, auto_now_add=False)
    end = models.DateTimeField(auto_now=False, auto_now_add=False)
    minpoint = models.IntegerField()
    howmany = models.IntegerField(default=5)


class UserAnswer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    ansewertext = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    iscorrect = models.BooleanField(default=False)


class ResultMember(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)
    all_answer = models.IntegerField()
    all_answer_correct = models.IntegerField()
    valid = models.BooleanField(default=False)


class Log(models.Model):
    STATUS_CHOICES = (
        ('l', 'login'),
        ('a', 'answerQuestion')
    )
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    logtime = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=1, choices=STATUS_CHOICES)