import uuid
from django.db import models


class BBQEvent(models.Model):
    organizer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateField()
    available_products = models.ManyToManyField('bbqproducts.BBQProduct')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        ordering = ['-date']


class BBQEventVisitor(models.Model):
    name = models.CharField(max_length=40)
    event = models.ForeignKey(BBQEvent, on_delete=models.CASCADE, related_name='visitors')
    guests_count = models.PositiveIntegerField(default=0)
    desired_products = models.ManyToManyField('bbqproducts.BBQProduct')
