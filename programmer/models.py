from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='images/')
    github = models.URLField(blank=True)
    introduction = models.TextField(blank=True)

    education_or_courses = models.TextField(blank=True)
    qualities = models.TextField()
    skills = models.TextField()

    def __str__(self):
        return 'Portfolio of' + self.user.first_name + " " + self.user.last_name
