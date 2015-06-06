import math
from django.db.models import F, Func, Sum, Case, When, ExpressionWrapper, FloatField
from django.shortcuts import render
from calcs import models
# Create your views here.

def show_events(request):
	return render(request, 'events.html', {"events": models.Event.objects.all()})

def event(request, eventId):
	event = models.Event.objects.get(pk=eventId)
	meals = list(models.MealsInEvent.objects.filter(FkEvent=eventId))
	ingredient_costs = models.PurchaseableItem.objects.filter(mealcomponent__Meal__event__id=eventId)\
		.distinct()\
		.annotate(quantity_needed = Sum(F('mealcomponent__AmountPerPerson') * F('mealcomponent__Meal__mealsinevent__AttendeeCount'), output_field=FloatField())) \
		.annotate(num_packages = Case(When(AlreadyHave__gt= F('quantity_needed') / F('QuantityProvided'), then=0),
			default=Func(0.49 - F('AlreadyHave') + (F('quantity_needed') / F('QuantityProvided')), output_field=FloatField(), function='ROUND'))) \
		.annotate(total_cost = ExpressionWrapper(F('num_packages') * F('UnitPrice'), output_field=FloatField())) \
		.values('quantity_needed', 'num_packages', 'total_cost', 'ItemName', 'AlreadyHave', 'QuantityProvided', 'PurchaseLink', 'QuantityUnits__Name')
	
	total_cost = 0
	for i in ingredient_costs:
		if i['total_cost'] > 0:
			total_cost += i['total_cost']
	return render(request, 'event.html',
	{
		"event": event,
		"meals": meals,
		"total_cost": total_cost,
		"ingredient_costs": ingredient_costs,
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