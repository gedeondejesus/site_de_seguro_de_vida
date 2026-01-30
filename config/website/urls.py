from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path("quote/", views.quote_page, name="quote"),
    path("api/calc-premium/", views.api_calc_premium, name="api_calc_premium"),
]
urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("plans/", views.plans, name="plans"),
    path("quote/", views.quote, name="quote"),
    path("contact/", views.contact, name="contact"),
    
]