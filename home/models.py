from django.utils import timezone
from django.db import models
from django.utils.text import slugify


# Create your models here.
class News(models.Model):
    image = models.ImageField(upload_to='news/', blank=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=70)
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = "Новости"
