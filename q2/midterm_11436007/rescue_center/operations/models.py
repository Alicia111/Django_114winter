from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

CATEGORY_CHOICES = [
    ('fire', 'fire'),
    ('flood', 'flood'),
    ('medical', 'medical'),
    ('power', 'power'),
    ('other', 'other'),
]

PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

STATUS_CHOICES = [
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('delivered', 'delivered'),
]


class Incident(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.pk} {self.title}"

    def get_absolute_url(self):
        return reverse('incident_detail', kwargs={'pk': self.pk})


class ResourceRequest(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='resource_requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_requests')
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} x{self.quantity} ({self.status})"


class ActionLog(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='action_logs')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_logs')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.incident}] {self.actor.username}: {self.note[:30]}"
