from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #
    #     super().save(*args, **kwargs)
