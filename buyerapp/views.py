from django.shortcuts import render
from django.http import request
from django.db.models import Q
from itertools import chain
from datetime import date
import re

from .models import City, Area, Property


def home(request):
	property_list = Property.objects.order_by('-upload_date')[:6]
	
	today = date.today()

	return render(request, 'buyer/index.html', {'cities': City.objects.all(), 'areas':Area.objects.all(),'property_list':property_list})   


def advance_search(request):
    return render(request, 'buyer/advance-search.html', {'cities': City.objects.all(), 'areas':Area.objects.all()})  


def foreclosure_search(request):
    return render(request, 'buyer/foreclosure.html', {'cities': City.objects.all(), 'areas':Area.objects.all()})  


def blog_search(request):
    return render(request, 'buyer/blog.html')  


def about_view(request):
    return render(request, 'buyer/aboutus.html')  
        

def contact_view(request):
    return render(request, 'buyer/contact.html')


def market_view(request):
    return render(request, 'buyer/market_report.html')


def property_search_view(request):
	# try:
		city = request.GET['CityChoice']
		area = request.GET['AreaChoice']
		lowprice = request.GET['LimitFrom']
		upprice = request.GET['LimitTo']

		if city and area and lowprice and upprice:
			property_list = Property.objects.filter((Q(city__exact=city) and Q(area__exact=area))).filter(Q(price__range=(lowprice, upprice)))
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city and area and lowprice:
			property_list = Property.objects.filter((Q(city__exact=city) and Q(area__exact=area))).filter(Q(price__gte=lowprice))
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city and area and upprice:
			property_list = Property.objects.filter((Q(city__exact=city) and Q(area__exact=area))).filter(Q(price__lte=upprice))
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city and area:
			property_list = Property.objects.filter(Q(city__exact=city) and Q(area__exact=area))
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city and lowprice:
			property_list = Property.objects.filter(city__name__exact=city).filter(price__gte=lowprice)
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city and upprice:
			property_list = Property.objects.filter(city__name__exact=city).filter(price__lte=upprice)
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif city:
			property_list = Property.objects.filter(city__name__contains=city)
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif lowprice and upprice:
			property_list = Property.objects.filter(Q(price__range=(lowprice, upprice)))
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif lowprice:
			property_list = Property.objects.filter(price__gte=lowprice)
			return render(request, 'buyer/property2.html', {'properties': property_list})
		elif upprice:
			property_list = Property.objects.filter(price__lte=upprice)
			return render(request, 'buyer/property2.html', {'properties': property_list})
		else:
			return render(request, 'buyer/property2.html', {'properties': Property.objects.all()})

	# except:
	# 	return render(request, 'buyer/property2.html', {'properties': Property.objects.all()})


def address_search_view(request):
	adrs_text = request.GET['address']
	property_list = list()
	if(adrs_text!=""):
		property_list = Property.objects.filter(property_address__icontains=adrs_text)

	return render(request, 'buyer/property2.html', {'properties': property_list})


def mls_search_view(request):
	mls_no = request.GET['mls_no']
	# print(mls_no)
	mls_list = mls_no.split(',')

	property_list = []
	for no in mls_list:
		no = Property.objects.filter(mls_no__exact=no)
		property_list = list(chain(no, property_list))

	# property_list = Property.objects.filter(mls_no__exact=mls_no)
	# print(property_list)
	return render(request, 'buyer/property2.html', {'properties': property_list})


def advanced_prop_search_view(request):
	property_query_set = Property.objects.all()
	city = request.GET.getlist("cityChoice")
	if("all" not in city):
		cities_list = City.objects.filter(name__in=city)
		property_query_set = property_query_set.filter(city__in= cities_list)

	arealist = request.GET.getlist("areaChoice")
	if("all" not in arealist):
		property_query_set = property_query_set.filter(area__in=arealist)
	
	property_type_list = request.GET.getlist("ptypeCheckbox")
	if(len(property_type_list)>0):
		print("property type:", property_type_list)
		property_query_set = property_query_set.filter(property_type__type__in=property_type_list)
	
	min_price=request.GET["minPricetxt"]
	if(min_price != "No Limit"):
		property_query_set = property_query_set.filter(price__gte=min_price)
	max_price=request.GET["maxPricetxt"]
	if(max_price != "No Limit"):
		property_query_set = property_query_set.filter(price__lte=max_price)

	size_in_sqfeet = request.GET["minSqfeettext"] 
	print(size_in_sqfeet)
	if(size_in_sqfeet !="" and size_in_sqfeet != "No Preference"):
		size_in_sqfeet = size_in_sqfeet.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_sqrfeet__gte=size_in_sqfeet)

	min_beds = request.GET["minBedtxt"] 
	if(min_beds !="" and min_beds != "Any"):
		min_beds = min_beds.replace("+","")
		property_query_set = property_query_set.filter(rooms__gte=min_beds)

	min_bath = request.GET["minBathtxt"] 
	if(min_bath !="" and min_bath != "Any"):
		min_bath = min_bath.replace("+","")
		property_query_set = property_query_set.filter(bathrooms__gte=min_bath)

	year_built = request.GET["builtYeartxt"] 
	if(year_built !="" and year_built != "No Preference"):
		year_built = year_built.replace("+","")
		property_query_set = property_query_set.filter(built_year__gte=year_built)		

	style = request.GET["styleTxt"] 
	if(style !="" and style != "All"):
		property_query_set = property_query_set.filter(style__option=style)

	foreclosure = request.GET["foreclosureTxt"] 
	if(foreclosure !="" and foreclosure != "No Preference"):
		if(foreclosure=='Yes'):
			foreclosure=True
		else:
			foreclosure=False	
		property_query_set = property_query_set.filter(Foreclosure=foreclosure)

	size_in_acre = request.GET["minAcrestxt"] 
	print(size_in_acre)
	if(size_in_acre !="" and size_in_acre != "No Preference"):
		size_in_acre = size_in_acre.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_acres__gte=size_in_acre)

	short_sale = request.GET["shortSaletxt"] 
	if(short_sale !="" and short_sale != "No Preference"):
		if(short_sale=='Yes'):
			short_sale=True
		else:
			short_sale=False	
		property_query_set = property_query_set.filter(short_sale=short_sale)

	print("-------city-----:",property_query_set)
	
	return render(request, 'buyer/property2.html', {'properties': property_query_set})



def condo_prop_search_view(request):
	property_query_set = Property.objects.all()
	city = request.GET.getlist("cityChoice")
	if("all" not in city):
		cities_list = City.objects.filter(name__in=city)
		property_query_set = property_query_set.filter(city__in= cities_list)

	arealist = request.GET.getlist("areaChoice")
	if("all" not in arealist):
		property_query_set = property_query_set.filter(area__in=arealist)
	
	building_list = request.GET.getlist("buildingChoice")
	if("all" not in building_list):
		property_query_set = property_query_set.filter(house__in=building_list)
	
	min_price=request.GET["minPricetxt"]
	if(min_price != "No Limit"):
		property_query_set = property_query_set.filter(price__gte=min_price)
	max_price=request.GET["maxPricetxt"]
	if(max_price != "No Limit"):
		property_query_set = property_query_set.filter(price__lte=max_price)

	size_in_sqfeet = request.GET["minSqfeettext"] 
	print(size_in_sqfeet)
	if(size_in_sqfeet !="" and size_in_sqfeet != "No Preference"):
		size_in_sqfeet = size_in_sqfeet.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_sqrfeet__gte=size_in_sqfeet)

	min_beds = request.GET["minBedtxt"] 
	if(min_beds !="" and min_beds != "Any"):
		min_beds = min_beds.replace("+","")
		property_query_set = property_query_set.filter(rooms__gte=min_beds)

	min_bath = request.GET["minBathtxt"] 
	if(min_bath !="" and min_bath != "Any"):
		min_bath = min_bath.replace("+","")
		property_query_set = property_query_set.filter(bathrooms__gte=min_bath)

	style = request.GET["styleTxt"] 
	if(style !="" and style != "All"):
		property_query_set = property_query_set.filter(style__option=style)

	

	print("-------city-----:",property_query_set)
	
	return render(request, 'buyer/property2.html', {'properties': property_query_set})
    


def foreclosure_search_view(request):
	property_query_set = Property.objects.filter(Foreclosure=True)

	city = request.GET.getlist("cityChoice")
	if("all" not in city):
		cities_list = City.objects.filter(name__in=city)
		property_query_set = property_query_set.filter(city__in= cities_list)

	arealist = request.GET.getlist("areaChoice")
	if("all" not in arealist):
		property_query_set = property_query_set.filter(area__in=arealist)
	
	property_type_list = request.GET.getlist("ptypeCheckbox")
	if(len(property_type_list)>0):
		print("property type:", property_type_list)
		property_query_set = property_query_set.filter(property_type__type__in=property_type_list)
	
	min_price=request.GET["minPricetxt"]
	if(min_price != "No Limit"):
		property_query_set = property_query_set.filter(price__gte=min_price)
	max_price=request.GET["maxPricetxt"]
	if(max_price != "No Limit"):
		property_query_set = property_query_set.filter(price__lte=max_price)

	size_in_sqfeet = request.GET["minSqfeettext"] 
	print(size_in_sqfeet)
	if(size_in_sqfeet !="" and size_in_sqfeet != "No Preference"):
		size_in_sqfeet = size_in_sqfeet.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_sqrfeet__gte=size_in_sqfeet)

	min_beds = request.GET["minBedtxt"] 
	if(min_beds !="" and min_beds != "Any"):
		min_beds = min_beds.replace("+","")
		property_query_set = property_query_set.filter(rooms__gte=min_beds)

	min_bath = request.GET["minBathtxt"] 
	if(min_bath !="" and min_bath != "Any"):
		min_bath = min_bath.replace("+","")
		property_query_set = property_query_set.filter(bathrooms__gte=min_bath)

	year_built = request.GET["builtYeartxt"] 
	if(year_built !="" and year_built != "No Preference"):
		year_built = year_built.replace("+","")
		property_query_set = property_query_set.filter(built_year__gte=year_built)		

	style = request.GET["styleTxt"] 
	if(style !="" and style != "All"):
		property_query_set = property_query_set.filter(style__option=style)

	size_in_acre = request.GET["minAcrestxt"] 
	print(size_in_acre)
	if(size_in_acre !="" and size_in_acre != "No Preference"):
		size_in_acre = size_in_acre.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_acres__gte=size_in_acre)


	print("-------city-----:",property_query_set)
	
	return render(request, 'buyer/property2.html', {'properties': property_query_set})


def zipcode_search_view(request):
	property_query_set = Property.objects.all()

	zip_list = request.GET.getlist("zipChoice")
	if("all" not in zip_list):
		property_query_set = property_query_set.filter(zipcode__in= zip_list)

	
	property_type_list = request.GET.getlist("ptypeCheckbox")
	if(len(property_type_list)>0):
		print("property type:", property_type_list)
		property_query_set = property_query_set.filter(property_type__type__in=property_type_list)
	
	min_price=request.GET["minPricetxt"]
	if(min_price != "No Limit"):
		property_query_set = property_query_set.filter(price__gte=min_price)
	max_price=request.GET["maxPricetxt"]
	if(max_price != "No Limit"):
		property_query_set = property_query_set.filter(price__lte=max_price)

	size_in_sqfeet = request.GET["minSqfeettext"] 
	print(size_in_sqfeet)
	if(size_in_sqfeet !="" and size_in_sqfeet != "No Preference"):
		size_in_sqfeet = size_in_sqfeet.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_sqrfeet__gte=size_in_sqfeet)

	min_beds = request.GET["minBedtxt"] 
	if(min_beds !="" and min_beds != "Any"):
		min_beds = min_beds.replace("+","")
		property_query_set = property_query_set.filter(rooms__gte=min_beds)

	min_bath = request.GET["minBathtxt"] 
	if(min_bath !="" and min_bath != "Any"):
		min_bath = min_bath.replace("+","")
		property_query_set = property_query_set.filter(bathrooms__gte=min_bath)

	style = request.GET["styleTxt"] 
	if(style !="" and style != "All"):
		property_query_set = property_query_set.filter(style__option=style)


	print("-------city-----:",property_query_set)
	
	return render(request, 'buyer/property2.html', {'properties': property_query_set})


def sold_search_view(request):
	property_query_set = Property.objects.filter(sale_type=2)
	city = request.GET.getlist("cityChoice")
	if("all" not in city):
		cities_list = City.objects.filter(name__in=city)
		property_query_set = property_query_set.filter(city__in= cities_list)

	arealist = request.GET.getlist("areaChoice")
	if("all" not in arealist):
		property_query_set = property_query_set.filter(area__in=arealist)
	
	property_type_list = request.GET.getlist("ptypeCheckbox")
	if(len(property_type_list)>0):
		print("property type:", property_type_list)
		property_query_set = property_query_set.filter(property_type__type__in=property_type_list)
	
	min_price=request.GET["minPricetxt"]
	if(min_price != "No Limit"):
		property_query_set = property_query_set.filter(price__gte=min_price)
	max_price=request.GET["maxPricetxt"]
	if(max_price != "No Limit"):
		property_query_set = property_query_set.filter(price__lte=max_price)

	size_in_sqfeet = request.GET["minSqfeettext"] 
	print(size_in_sqfeet)
	if(size_in_sqfeet !="" and size_in_sqfeet != "No Preference"):
		size_in_sqfeet = size_in_sqfeet.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_sqrfeet__gte=size_in_sqfeet)

	min_beds = request.GET["minBedtxt"] 
	if(min_beds !="" and min_beds != "Any"):
		min_beds = min_beds.replace("+","")
		property_query_set = property_query_set.filter(rooms__gte=min_beds)

	min_bath = request.GET["minBathtxt"] 
	if(min_bath !="" and min_bath != "Any"):
		min_bath = min_bath.replace("+","")
		property_query_set = property_query_set.filter(bathrooms__gte=min_bath)

	year_built = request.GET["builtYeartxt"] 
	if(year_built !="" and year_built != "No Preference"):
		year_built = year_built.replace("+","")
		property_query_set = property_query_set.filter(built_year__gte=year_built)		

	style = request.GET["styleTxt"] 
	if(style !="" and style != "All"):
		property_query_set = property_query_set.filter(style__option=style)

	size_in_acre = request.GET["minAcrestxt"] 
	print(size_in_acre)
	if(size_in_acre !="" and size_in_acre != "No Preference"):
		size_in_acre = size_in_acre.replace("+","")
		property_query_set = property_query_set.filter(property_size_in_acres__gte=size_in_acre)


	print("-------city-----:",property_query_set)
	
	return render(request, 'buyer/property2.html', {'properties': property_query_set})



