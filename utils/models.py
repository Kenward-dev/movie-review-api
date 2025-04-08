import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Base model for all models in the application.
    Provides common fields like uuid, created_at and updated_at.
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the object"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the object was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the object was last updated"
    )
    
    class Meta:
        abstract = True
