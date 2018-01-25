import six
import copy

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from printapp.models import Printer


class CustomNestingField(serializers.Field):

	def __init__(self, field_name, attrs, *args, **kwargs):
		super(CustomNestingField, self).__init__(*args, **kwargs)
		self.field_name = field_name
		self.attrs = attrs

	def to_internal_value(self, data):
		if not isinstance(self.field_name, six.string_types):
			msg = 'Incorrect type. Expected a string, but got %s'
			raise ValidationError(msg % type(self.field_name).__name__)
		
		if not isinstance(data, dict):
			msg = 'Incorrect type. Expected a dict, but got %s'
			raise ValidationError(msg % type(data).__name__)
		else:
			if data.keys() != self.attrs.keys():
				msg = 'Informed keys are %s, but should be %s'
				raise ValidationError(msg % (data.keys(), self.attrs.keys()))

			for key in data.keys():
				if not isinstance(key, six.string_types):
					msg = 'Incorrect type. Expected a string, but got %s'
					raise ValidationError(msg % type(key).__name__)
				else:
					if key not in self.attrs.keys():
						msg = '%s is not part of %s'
						raise ValidationError(msg % (key, self.attrs.keys()))
			
			for value in data.values():
				if not isinstance(value, six.integer_types):
					msg = 'Incorrect type. Expected a integer, but got %s'
					raise ValidationError(msg % type(value).__name__)

		field_attrs = {}

		for attr_key, attr_value in self.attrs.iteritems():
			field_attrs[attr_value] = data[attr_key]

		return field_attrs

	def to_representation(self, obj):
		return obj


class NestingSerializer(serializers.Serializer):
	nesting = {
		"productionTime": {
			"minimum": "min_production_time",
			"maximum": "max_production_time",
		}
	}

	def __init__(self, *args, **kwargs):
		super(NestingSerializer, self).__init__(*args, **kwargs)
		self._build_fields()

	def _build_fields(self):
		for field_name, field_attributes in self.nesting.iteritems():
			self._perform_build_field(field_name, field_attributes)
			self._delete_fields(field_attributes)

	def _perform_build_field(self, field_name, field_attributes):
		self.fields[field_name] = CustomNestingField(source='*', field_name=field_name, attrs=field_attributes)
		print self.fields[field_name].to_representation(self.instance)

	def _delete_fields(self, field_attributes):
		fields_to_be_deleted = set()
		for value in field_attributes.values():
			if isinstance(value, (str, unicode)):
				fields_to_be_deleted.add(value)
		for field in fields_to_be_deleted:
			del self.fields[field]

	def _replace_item(self, data, value, replace_value):
		for k, v in data.items():
			if isinstance(v, dict):
				data[k] = self._replace_item(v, value, replace_value)
		if value in data.values():
			key = data.keys()[data.values().index(value)]
			data[key] = replace_value
		return data

	def to_representation(self, obj):
		data = super(NestingSerializer, self).to_representation(obj)

		nesting_dict = copy.deepcopy(self.nesting)
		nesting_dict = self._replace_item(nesting_dict, 'min_production_time', obj.min_production_time)
		nesting_dict = self._replace_item(nesting_dict, 'max_production_time', obj.max_production_time)

		data.update(nesting_dict)
		return data


class PrinterSerializer(NestingSerializer, serializers.ModelSerializer):
	
	class Meta:
		model = Printer
		fields = ('name', 'min_production_time', 'max_production_time')

	def validate(self, data):
		data = super(PrinterSerializer, self).validate(data)
		if data['min_production_time'] > data['max_production_time']:
			raise serializers.ValidationError("Min. production time cannot be greater than Max. production time")
		return data
