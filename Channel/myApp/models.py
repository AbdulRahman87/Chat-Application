from django.db import models

# Create your models here.

class Chat(models.Model):
    message = models.TextField()
    user = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message

class Group(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name