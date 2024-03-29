from django.db import models
from django.utils import timezone


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    positive_version = models.TextField(blank=True, null=True)
    find_pattern = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Entries"
