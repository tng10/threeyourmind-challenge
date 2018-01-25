# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Printer(models.Model):
	# Name of the Printer
	name = models.CharField(max_length=100)
	# minimum time (in minutes) the printer needs to produce a part
	min_production_time = models.IntegerField()
	# maximum time (in minutes) the printer needs to produce a part
	max_production_time = models.IntegerField()
