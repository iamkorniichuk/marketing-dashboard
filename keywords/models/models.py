from django.db import models


class Keyword(models.Model):
    text = models.CharField(max_length=256)
    is_generated_by_chat_gpt = models.BooleanField(default=False)

    def __str__(self):
        return self.text
