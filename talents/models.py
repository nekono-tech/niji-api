from django.db import models

class Talent(models.Model):
    name = models.CharField(max_length=100, default='')
    name_en = models.CharField(max_length=100, default='')
    slug = models.CharField(max_length=100, default='')
    debut_at = models.DateTimeField(null=True, default=None)
    fanclub_url = models.URLField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'talents'