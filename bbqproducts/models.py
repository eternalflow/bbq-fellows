from django.db import models


class BBQProduct(models.Model):
    type_name = models.CharField(default="Meat", max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name