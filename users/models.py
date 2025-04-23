from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Water Delivery', 'Water Delivery'),
        ('Construction Equipment', 'Construction Equipment'),
        ('Transport', 'Transport'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.provider.username}"
