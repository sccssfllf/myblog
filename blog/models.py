from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class ModelPost(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)

    # For the future:
    views = models.PositiveBigIntegerField(default=0)  # Views count
    # Temporarily str, later will be replaced with TaggableManager
    tags = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:

            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ModelPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if not self.published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date', '-created_at']
