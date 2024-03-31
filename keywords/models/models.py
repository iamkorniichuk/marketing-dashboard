from django.db import models


class Keyword(models.Model):
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text
