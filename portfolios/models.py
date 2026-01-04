from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base model with created_at and updated_at fields.
    
    All models in the application should inherit from this base model
    to ensure consistent timestamp tracking.
    """
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
