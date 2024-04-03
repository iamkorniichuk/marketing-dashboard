from django.db import models


class BaseKeyword(models.Model):
    text = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.text


class UserKeyword(BaseKeyword):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    pass


class ChatGptKeyword(BaseKeyword):
    class Meta:
        verbose_name = "ChatGPT"
        verbose_name_plural = "ChatGPT"

    based_on = models.ManyToManyField(BaseKeyword, related_name="chat_gpt_keywords")
