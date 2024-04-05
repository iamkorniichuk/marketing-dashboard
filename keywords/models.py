import re

from django.db import models


def preprocess_keyword(text):
    return re.sub(r"[^\w\s]", " ", text)


class BaseKeyword(models.Model):
    text = models.CharField(max_length=256, unique=True)

    def save(self, *args, **kwargs):
        self.text = preprocess_keyword(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class UserKeyword(BaseKeyword):
    class Meta:
        verbose_name = "User Keyword"
        verbose_name_plural = "User"

    pass


class ChatGptKeyword(BaseKeyword):
    class Meta:
        verbose_name = "ChatGPT Keyword"
        verbose_name_plural = "ChatGPT"

    based_on = models.ManyToManyField(BaseKeyword, related_name="chat_gpt_keywords")
