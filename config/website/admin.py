from django.contrib import admin
from .models import Banner, HomeCard, GalleryImage
from django.contrib import admin
from .models import CoverageAmount, PremiumRate, QuoteFactor, QuoteRequest

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    search_fields = ("title",)

@admin.register(HomeCard)
class HomeCardAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")




@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    


@admin.register(CoverageAmount)
class CoverageAmountAdmin(admin.ModelAdmin):
    list_display = ("label", "amount")
    search_fields = ("label",)
    ordering = ("amount",)

@admin.register(PremiumRate)
class PremiumRateAdmin(admin.ModelAdmin):
    list_display = ("gender", "age", "coverage", "monthly_premium")
    list_filter = ("gender", "coverage")
    search_fields = ("age", "coverage__label")
    ordering = ("gender", "age", "coverage__amount")

@admin.register(QuoteFactor)
class QuoteFactorAdmin(admin.ModelAdmin):
    list_display = ("key", "multiplier")
    list_editable = ("multiplier",)
    ordering = ("key",)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "gender", "age", "coverage", "smoker", "health_level", "calculated_monthly", "created_at")
    list_filter = ("gender", "smoker", "health_level", "coverage")
    search_fields = ("full_name", "email")
    ordering = ("-created_at",)
     