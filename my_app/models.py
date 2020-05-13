from django.db import models


class Search(models.Model):
    search = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.search}'

    class Meta:
        verbose_name_plural = 'Searches'
