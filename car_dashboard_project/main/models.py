from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
        ('analyst', 'Аналитик'),
    ]
    TYPE_CHOICES = [
        ('individual', 'Физическое лицо'),
        ('company', 'Юридическое лицо')
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    user_type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True)
    
    # Для физлица
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    
    # Для юрлица
    company_name = models.CharField(max_length=255, blank=True, null=True)
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_photos/', blank=True, null=True, default='img/default_user_img.png')

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