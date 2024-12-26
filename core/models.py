from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="specialities/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('doctors:list') + f'?speciality={self.slug}'

    @property
    def doctor_count(self):
        return self.doctor_set.filter(is_active=True).count()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/assets/img/specialities/default.png"
