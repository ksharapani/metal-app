from django.db import models


class Metal(models.Model):
    objects = None

    metal_name = models.CharField(max_length=512)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.metal_name


class Value(models.Model):
    objects = None

    value = models.FloatField()
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.value)
