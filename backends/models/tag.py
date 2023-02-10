from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='tag')

    class Meta:
        app_label = 'backends'

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.name)
