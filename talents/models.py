from django.db import models

class Talent(models.Model):
    name = models.CharField(max_length=100, default='')
    name_en = models.CharField(max_length=100, default='')
    name_ruby = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    slug = models.CharField(max_length=100, default='')
    debut_at = models.DateTimeField(null=True, default=None)
    affiliation = models.CharField(max_length=20, default='')
    birthday = models.CharField(max_length=20, default='')
    fan_name = models.CharField(max_length=100, default='')
    youtube_id = models.CharField(max_length=100, default='')
    x_id = models.CharField(max_length=100, default='')
    twitch_id = models.CharField(max_length=100, default='')
    funclub_id = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'talents'