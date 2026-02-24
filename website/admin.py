from django.contrib import admin
from .models import Banner, HomeCard, GalleryImage, Testimonial, VideoTestimonial, TermRate


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    ordering = ("order",)
    search_fields = ("title",)


@admin.register(HomeCard)
class HomeCardAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    ordering = ("order",)
    search_fields = ("title",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    ordering = ("order",)
    search_fields = ("title",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_active", "allow_publish", "is_approved", "created_at")
    list_display_links = ("name",)
    list_filter = ("is_active", "allow_publish", "is_approved", "rating")
    search_fields = ("name", "text")
    list_editable = ("is_active", "allow_publish", "is_approved")
    ordering = ("-created_at",)


@admin.register(VideoTestimonial)
class VideoTestimonialAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active", "allow_publish", "is_approved", "created_at")
    list_display_links = ("title",)
    list_filter = ("is_active", "allow_publish", "is_approved")
    search_fields = ("title", "youtube_url")
    list_editable = ("order", "is_active", "allow_publish", "is_approved")
    ordering = ("order", "-created_at")


@admin.register(TermRate)
class TermRateAdmin(admin.ModelAdmin):
    list_display = ("gender", "age", "coverage", "smoker", "price")
    list_filter = ("gender", "smoker", "coverage")
    search_fields = ("age", "coverage")
    ordering = ("gender", "age", "coverage")
