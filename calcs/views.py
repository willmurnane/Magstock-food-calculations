import math
from django.db.models import F, Sum
from django.shortcuts import render
from calcs import models
# Create your views here.

def show_events(request):
	return render(request, 'events.html', {"events": models.Event.objects.all()})

def event(request, eventId):
	from django.db import connection
#	ingredients = models.MealComponent.objects.filter(Meal__event__id = eventId).annotate(total_ing=Sum(F('AmountPerPerson')))
	ingredients = models.PurchaseableItem.objects.filter(mealcomponent__Meal__event__id=eventId)
	return render(request, 'event.html',
	{
		"event": models.Event.objects.get(pk=eventId),
		"meals": models.MealsInEvent.objects.filter(FkEvent=eventId),
		"ingredients": ingredients,
	})

def mealcost(request, mealInEventId):
	mie = models.MealsInEvent.objects.select_related('FkMeal').get(pk=mealInEventId)
	scaledComponents = []
	totalCost = 0
	for comp in models.MealComponent.objects.filter(Meal=mie.FkMeal).select_related('Ingredient', 'Ingredient__QuantityUnits'):
		total = comp.AmountForGroup + (comp.AmountPerPerson * mie.AttendeeCount)
		purchaseIncrement = comp.Ingredient.QuantityProvided
		numToPurchase = math.ceil(total / purchaseIncrement)
		itemCost = numToPurchase * comp.Ingredient.UnitPrice
		totalCost += itemCost
		scaledComponents.append({
				"Name": comp.Ingredient.ItemName,
				"AmountPerPerson": comp.AmountPerPerson,
				"AmountForGroup": comp.AmountForGroup,
				"Units": comp.Units.Name,
				"TotalAmount": total,
				"PurchaseIncrement": purchaseIncrement,
				"NumberToPurchase": numToPurchase,
				"ItemCost": itemCost,
			})
	return render(request, 'cost.html',
	{
		"mealInEvent": mie,
		"scaledComponents": scaledComponents,
		"TotalCost": totalCost,
	})