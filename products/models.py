from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Represents a car or spare part listing in the marketplace.
    Every product is owned by a registered user.
    """

    CATEGORY_CHOICES = (
        ('car', 'Car'),
        ('spare_part', 'Spare Part'),
    )

    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name        = models.CharField(max_length=255)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand       = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default='')
    year        = models.PositiveIntegerField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']   # newest first everywhere by default

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year or 'N/A'})"