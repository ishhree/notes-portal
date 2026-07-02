from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    pdf = models.FileField(upload_to='notes/', null=True, blank=True)
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title