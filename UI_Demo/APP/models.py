# models.py

from django.db import models

class chat_Model(models.Model):
    chat_user = models.TextField()
    chat_system = models.TextField()

    def __str__(self):
        return f"{self.chat_user} | {self.chat_system}"

