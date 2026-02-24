import re
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator




class VideoTestimonial(models.Model):
    title = models.CharField(max_length=120, blank=True)
    youtube_url = models.URLField()
    allow_publish = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or self.youtube_url

    def youtube_id(self):
        url = (self.youtube_url or "").strip()
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0].split("&")[0].split("/")[0]
        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        if "/embed/" in url:
            return url.split("/embed/")[1].split("?")[0].split("&")[0].split("/")[0]
        if "/shorts/" in url:
            return url.split("/shorts/")[1].split("?")[0].split("&")[0].split("/")[0]
        return ""


# =========================
# TESTIMONIAL (TEXTO)
# =========================
class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 1..5
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    allow_publish = models.BooleanField(default=False)  # cliente autorizou
    is_approved = models.BooleanField(default=False)    # admin aprovou
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


# =========================
# HOME CONTENT
# =========================
class Banner(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} - {self.title}"


class HomeCard(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    image = models.ImageField(upload_to="cards/", blank=True, null=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="gallery/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} - {self.title or 'Gallery Image'}"


# =========================
# QUOTE / RATES
# =========================
class CoverageAmount(models.Model):
    label = models.CharField(max_length=30, unique=True)  # "300 mil"
    amount = models.PositiveIntegerField(unique=True)     # 300000

    class Meta:
        ordering = ["amount"]

    def __str__(self):
        return self.label


class PremiumRate(models.Model):
    GENDER_CHOICES = [
        ("F", "Mulher"),
        ("M", "Homem"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    coverage = models.ForeignKey(CoverageAmount, on_delete=models.CASCADE, related_name="rates")
    monthly_premium = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("gender", "age", "coverage")
        ordering = ["gender", "age", "coverage__amount"]

    def __str__(self):
        return f"{self.get_gender_display()} | {self.age} | {self.coverage.label} = {self.monthly_premium}"


class QuoteFactor(models.Model):
    KEY_CHOICES = [
        ("SMOKER_NO", "Fumante: Não"),
        ("SMOKER_YES", "Fumante: Sim"),
        ("HEALTH_OK", "Saúde: Sem problemas"),
        ("HEALTH_LIGHT", "Saúde: Leve"),
        ("HEALTH_MED", "Saúde: Moderado"),
        ("HEALTH_HIGH", "Saúde: Grave"),
    ]

    key = models.CharField(max_length=30, choices=KEY_CHOICES, unique=True)
    multiplier = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("1.00"))

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return f"{self.get_key_display()} ({self.multiplier}x)"


class QuoteRequest(models.Model):
    GENDER_CHOICES = [("F", "Mulher"), ("M", "Homem")]
    HEALTH_CHOICES = [
        ("OK", "Sem problemas"),
        ("LIGHT", "Leve"),
        ("MED", "Moderado"),
        ("HIGH", "Grave"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    coverage = models.ForeignKey(CoverageAmount, on_delete=models.PROTECT)
    smoker = models.BooleanField(default=False)
    health_level = models.CharField(max_length=10, choices=HEALTH_CHOICES, default="OK")
    health_details = models.TextField(blank=True)

    calculated_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email} ({self.created_at:%Y-%m-%d})"


class TermRate(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    coverage = models.IntegerField()
    smoker = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("gender", "age", "coverage", "smoker")
        ordering = ["gender", "age", "coverage", "smoker"]

    def __str__(self):
        return f"{self.gender} | age={self.age} | cov={self.coverage} | smoker={self.smoker} | ${self.price}"
