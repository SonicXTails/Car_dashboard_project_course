from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
        ('analyst', 'Аналитик'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)  # номер телефона

    @property
    def days_on_site(self):
        delta = now() - self.date_joined
        return delta.days
    
class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title