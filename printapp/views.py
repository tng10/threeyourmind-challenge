# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from printapp.models import Printer
from printapp.serializers import PrinterSerializer


class PrinterViewSet(viewsets.ModelViewSet):
	"""
	A simple ViewSet for viewing and editing accounts.
	"""
	queryset = Printer.objects.all()
	serializer_class = PrinterSerializer
