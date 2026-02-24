
from django.urls import path
from . import views
from . views import home
from django.contrib import admin
from website.views_admin import admin_logout_view

urlpatterns = [
    path("admin/logout/", admin_logout_view, name="custom_admin_logout"),
    path("admin/", admin.site.urls),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("plans/", views.plans, name="plans"),
    path("contact/", views.contact, name="contact"),
    path("quote/", views.quote_page, name="quote"),

    # API
    path("api/calc-premium/", views.api_calc_premium, name="api_calc_premium"),
]
