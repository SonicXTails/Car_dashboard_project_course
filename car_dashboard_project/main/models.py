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
    profile_image = models.ImageField(
        upload_to='profile_photos/', 
        blank=True, 
        null=True, 
        default='img/default_user_img.png'
    )

    @property
    def days_on_site(self):
        return (now() - self.date_joined).days


class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserReview(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_left')
    reviewed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed')


class UserAuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Создание'),
        ('update', 'Изменение'),
        ('delete', 'Удаление'),
        ('block', 'Блокировка'),
    ]

    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_table = models.CharField(max_length=255)
    target_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class AnalyticsEvent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='analytics_events')
    event_type = models.CharField(max_length=100)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SiteVisit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='site_visits')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)