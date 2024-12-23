from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
# Create your models here.
from django.db.models import Count
from datetime import datetime


from django.db import models

class forummodel(models.Model):
    ForumTitile = models.CharField(max_length=50, unique=True)
    ForumDescription = models.CharField(max_length=150)
    ForumImage = models.ImageField(
        upload_to='board_images/',       # Directory within MEDIA_ROOT
        null=True,                       # Allow null values in the database
        blank=True,                      # Allow leaving the field blank in forms
        default='board_images/bootstrap.png'  # Path to the default image
    )

    # image = models.ImageField(upload_to='board_images/', null=True, blank=True)

    def __str__(self):
        return self.ForumTitile
    def  gtc(self):
        return ForumSectionModel.objects.filter(board__ForumTitile=self).count()
    def gpc(self):
        return CommentModel.objects.filter(section__board=self).count()

    def glp(self):
        return CommentModel.objects.filter(section__board=self).order_by('-created_dt').first()

    def g(self):
        # Define the start and end of November
        start_date = datetime(year=2023)
        end_date = datetime(year=2024)

        # Count ForumSectionModel entries related to the current forummodel instance within November
        return ForumSectionModel.objects.filter(
            board=self,  # Filter by the current forummodel instance
            created_dt__range=(start_date, end_date)
        ).count()

class ForumSectionModel(models.Model):
    SectionSubject = models.CharField(max_length=255)
    board = models.ForeignKey(forummodel,related_name='forms',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='forms',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    updated_by = models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)
    updated_dt = models.DateTimeField(null=True)

    def __str__(self):
        return self.SectionSubject

class CommentModel(models.Model):
    massg = models.TextField(max_length=4000)
    section = models.ForeignKey(ForumSectionModel,related_name='comt',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='comt',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)
    updated_dt = models.DateTimeField(null=True)
    def __str__(self):
        truncted_message = Truncator(self.massg)
        return truncted_message.chars(30)
    
  
  