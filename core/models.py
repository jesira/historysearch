from django.db import models
from django.utils import timezone

class History(models.Model):
    user = models.CharField(max_length = 120)
    keyword = models.CharField(max_length = 120)
    result = models.CharField(max_length = 500)
    searched_time = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user
