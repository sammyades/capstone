from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

# Role model
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# User model
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


# Lead model
class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal Sent"),
        ("negotiation", "Negotiation"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="owned_leads", null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=False, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Nigeria")
    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return f"{self.company} - {self.status}"


# Deal opportunity model
class Deal(models.Model):

    STATUS_CHOICES = [
        ("open", "Open"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]
    STAGE_CHOICES = [
        ("qualification", "Qualification"),
        ("proposal", "Proposal Sent"),
        ("negotiation", "Negotiation"),
        ("review", "Contract Review"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="owned_deal")
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="deal")
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default="qualification")
    expected_close_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return f"Deal - {self.lead.company if self.lead else 'Converted Account'}"

@receiver(post_delete, sender=Deal)
def reset_lead_status_on_deal_deletion(sender, instance, **kwargs):
    """
    When a Deal is deleted, find the associated lead, 
    check if it has any other remaining deals, and revert its status if empty.
    """
    lead = instance.lead
    if lead:
        # Check if this lead has any OTHER deals left
        if not lead.deal.exists():
            lead.status = 'NEW'  # Change this to match your exact "New" choice value
            lead.save()

# Task Model
class Task(models.Model):

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="tasks")
    deal = models.ForeignKey('Deal', on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Activity model
class Activity(models.Model):

    ACTIVITY_TYPE = [
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("visit", "Visit"),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="activities")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="owned_activities")

    type = models.CharField(max_length=20, choices=ACTIVITY_TYPE)
    note = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type} - {self.lead.company}"
