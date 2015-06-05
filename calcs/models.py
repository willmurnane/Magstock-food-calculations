from django.db import models
import datetime

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
	AlreadyHave = models.IntegerField(default=0, blank=True)
	PriceUpdatedDate = models.DateField(default=datetime.date.today)
	def __str__(self):
		return self.ItemName

class Meal(models.Model):
	Name = models.CharField(max_length=100)
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
	AmountForGroup = models.FloatField(default=0,blank=True)

	def __str__(self):
		return "%s -> %s: %s%s per person%s" % \
			(self.Meal, self.Ingredient.ItemName, self.AmountPerPerson, self.Units,
			"" if self.AmountForGroup == 0 else ", %s%s for group" % (self.AmountForGroup, self.Units))

class Event(models.Model):
	Name = models.CharField(max_length=100)
	Meals = models.ManyToManyField(Meal, through='MealsInEvent')
	def __str__(self):
		return self.Name

class MealsInEvent(models.Model):
	FkEvent = models.ForeignKey(Event)
	FkMeal = models.ForeignKey(Meal)
	AttendeeCount = models.IntegerField() 
	def __str__(self):
		return "At %s: %d people for %s" % (self.FkEvent.Name, self.AttendeeCount, self.FkMeal.Name)



