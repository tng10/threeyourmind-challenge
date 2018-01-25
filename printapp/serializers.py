from rest_framework import serializers
from printapp.models import Printer


class PrinterSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Printer
		fields = ('name', 'min_production_time', 'max_production_time')

	def to_representation(self, obj):
		return {
			"name": obj.name,
			"productionTime": {
				"minimum": obj.min_production_time,
				"maximum": obj.max_production_time,
			}
		}

	def validate(self, data):
		"""
		Check that the start is before the stop.
		"""
		data = super(PrinterSerializer, self).validate(data)
		if data['min_production_time'] > data['max_production_time']:
			raise serializers.ValidationError("Min. production time cannot be greater than Max. production time")
		return data
