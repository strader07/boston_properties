from django.db import models
from datetime import date


class Property(models.Model):
    name = models.CharField(max_length=400)
    house = models.CharField(max_length=200)
    user = models.CharField(max_length=100, null=True)
    upload_date = models.DateField(default=date.today)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    property_address = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=15)
    lattitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    property_type = models.ForeignKey('PropertyType',on_delete=models.CASCADE)
    sale_type = models.ForeignKey('SaleStatus', on_delete=models.CASCADE)
    furnished = models.BooleanField(null=True)
    price = models.FloatField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garden = models.BooleanField(null=True, default=False)
    pool = models.BooleanField(null=True, default=False)
    parking = models.BooleanField(null=True, default=False)
    property_desc = models.TextField()
    location_desc = models.TextField()
    style = models.ForeignKey('Style', on_delete=models.CASCADE)
    built_year = models.IntegerField()
    short_sale= models.BooleanField()
    Foreclosure= models.BooleanField()
    property_size_in_sqrfeet = models.FloatField()
    property_size_in_acres= models.FloatField()
    mls_no = models.CharField(max_length=30, null=True)
    # floorplan = models.ForeignKey('FloorPlan', default='None',on_delete=models.CASCADE)
    featured = models.BooleanField()
    # image_gallery = models.ForeignKey(Gallery, default='None', on_delete=models.CASCADE)
    property_image= models.ImageField()
    area = models.CharField(max_length=220)

    def __str__(self):
        return self.name

	
    def get_city_name(self):
        return self.city.name

    def get_property_type(self):
        return property_type.type

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class PropertyType(models.Model):
    """ type like land, house or condo"""
    type = models.CharField(max_length=150,  unique=True)  
    
    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Type"


class SaleStatus(models.Model):
    """ sold or active..."""
    value = models.CharField(max_length=150,  unique=True)  

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Sales Status"
        verbose_name_plural = "Sales Status"


class Style(models.Model):
    """ like duplex or flat """
    option = models.CharField(max_length=150, unique=True)  

    def __str__(self):
        return self.option

    class Meta:
        verbose_name = "Property Style"
        verbose_name_plural = "Style"


class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "City"

class Area(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    area_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.area_name


    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Area"
