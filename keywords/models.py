from django.db import models


class CrossroadsKeyword(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign_id", "lander_keyword", "date"],
                name="crossroads_unique_keyword_for_date",
            )
        ]

    campaign_id = models.CharField(max_length=128)
    lander_keyword = models.CharField(max_length=128)
    clicks = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.lander_keyword
