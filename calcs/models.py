from django.db import models

class Unit(models.Model):
	Name = models.CharField(max_length=10)
	def __str__(self):
		return self.Name

class PurchaseableItem(models.Model):
	ItemName = models.CharField(max_length=200)
	UnitPrice = models.DecimalField(max_digits=6, decimal_places=2)
	QuantityProvided = models.FloatField(default = 1)
	QuantityUnits = models.ForeignKey(Unit)
	PurchaseLink = models.CharField(max_length=1024, blank=True, null=True)
	def __str__(self):
		return self.ItemName

class Meal(models.Model):
	Name = models.CharField(max_length=100)
	Attendees = models.IntegerField()
	def __str__(self):
		return self.Name

class MealComponent(models.Model):
	Meal = models.ForeignKey(Meal)
	Ingredient = models.ForeignKey(PurchaseableItem)
	def _units(self):
		return self.Ingredient.QuantityUnits
	_units.boolean = True
	Units = property(_units)
	AmountPerPerson = models.FloatField()
	AmountForGroup = models.FloatField()

	def __str__(self):
		return "%s -> %s: %s%s per person, %s%s for group" % \
			(self.Meal, self.Ingredient.ItemName, self.AmountPerPerson, self.Units, self.AmountForGroup, self.Units)
