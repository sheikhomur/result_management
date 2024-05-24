from django.db import models
import time, random, string


class UniqueIDModel(models.Model):
    def generate_unique_id():
        epoch = int(time.time())
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        # this will be 100% unique
        return f"{random_str}{epoch}"

    id = models.CharField(max_length=15, unique=True, editable=False, primary_key=True,
        default=generate_unique_id)
    class Meta:
        abstract = True


class TrackingModel(UniqueIDModel):
    """By inheriting this model, we get created and updated time out of the box"""
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

