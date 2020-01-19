from django.db import models

app_label = "common"

class Result(models.Model):
    string = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    error = models.CharField(max_length=200, null=True)
