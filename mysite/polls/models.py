import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib import admin
from django.db import models
from django.utils import timezone

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class Question(models.Model):
    """
    Represents a question in the poll with a text and publication dates.
    
    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date when the question was published.
        end_date (datetime): The date when the question ends (optional).
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', blank=True, null=True)
    
    def __str__(self):
        """
        Returns a string representation of the question.
        
        Returns:
            str: The text of the question.
        """
        return self.question_text
    
    def is_published(self):
        """
        Determines if the question is published.
        
        Returns:
            bool: True if the question is published; otherwise, False.
        """
        return self.pub_date <= timezone.now()
    
    def was_published_recently(self):
        """
        Determines if the question was published within the last day.
        
        Returns:
            bool: True if the question was published within the last day; otherwise, False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def can_vote(self):
        """
        Determines if voting is allowed for the question based on its publication and end dates.
        
        Returns:
            bool: True if voting is allowed; otherwise, False.
        """
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Display whether the question was published recently for the admin interface.
        
        Returns:
            bool: True if the question was published within the last day; otherwise, False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    """
    Represents a choice for a question in the poll.
    
    Attributes:
        question (Question): The question that this choice belongs to.
        choice_text (str): The text of the choice.
        votes (int): The number of votes for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()

    
    def __str__(self):
        """
        Returns a string representation of the choice.
        
        Returns:
            str: The text of the choice.
        """
        return self.choice_text
    
class Vote(models.Model):
    """Record a choice for a question made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted on {self.choice.question}"