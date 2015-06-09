from django import forms
from django.forms import widgets
from calcs import models

class MealAndQuantityPicker(widgets.Widget):
	def __init__(self, attrs=None):
		self.attrs = attrs
		self.meal = widgets.Select()
	def render(self, name, value, attrs=None):
		self.meal.render(name, value, attrs)

class EventForm(forms.ModelForm):
	class Meta:
		model = models.Event
		fields = ['Name', 'Meals']
		widgets = {
			"Meals": MealAndQuantityPicker,
			}