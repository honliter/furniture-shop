from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Furniture(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, default='🪑')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title
