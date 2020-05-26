# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DummyTrip(models.Model):
    operator_name = models.CharField(max_length=255)
    polyline = models.TextField()
    shuttle_identifier = models.CharField(max_length=255)
