from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

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

class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField(null=True, blank=True)  # optional: when they want the service
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')

    def __str__(self):
        return f"{self.client.username} booked {self.service.name}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.subject}"