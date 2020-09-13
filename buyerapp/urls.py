from django.contrib import admin
from django.urls import path
from .views import *



urlpatterns = [
    path('', home),
    path('advance-search', advance_search),
    path('foreclosures', foreclosure_search),
    path('social-media', blog_search),
    path('about', about_view),
    path('contact', contact_view),
    path('market_report', market_view),
    path('property_result', property_search_view),
    path('address_result', address_search_view),
    path('mls_result', mls_search_view),
    path('advanced-search-result', advanced_prop_search_view),
    path('condo-search-result', condo_prop_search_view),
    path('foreclosure-search-result', foreclosure_search_view),
    path('zipcode-search-result', zipcode_search_view),
    path('sold-search-result', sold_search_view),

]
