from django.db import models
from django.contrib.auth.models import User


class Anime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    eng_name = models.CharField(max_length=200, blank=False, null=True)
    director_name = models.CharField(max_length=100, blank=False, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    episodes_number = models.IntegerField(blank=True, null=True)
    is_based_on_manga = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.eng_name
