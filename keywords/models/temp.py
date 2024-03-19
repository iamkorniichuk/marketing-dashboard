from django.db import models


class TempCrossroadsKeyword(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign_id", "lander_keyword", "date"],
                name="crossroads_unique_keyword_for_date",
            )
        ]
        managed = False

    campaign_id = models.CharField(max_length=128)
    lander_keyword = models.CharField(max_length=128)
    clicks = models.IntegerField()
    date = models.DateField()
