from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def update(self, text: str):
        self.chat = text
        self.save()
