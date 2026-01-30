from django.db import models


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

    image = models.ImageField(
        upload_to="cards/",
        blank=True,
        null=True
    )

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
    
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class CoverageAmount(models.Model):
    """
    Ex: 300 mil, 500 mil, 700 mil, 1M
    """
    label = models.CharField(max_length=30, unique=True)  # "300 mil"
    amount = models.PositiveIntegerField(unique=True)     # 300000

    class Meta:
        ordering = ["amount"]

    def __str__(self):
        return self.label


class PremiumRate(models.Model):
    """
    Valor BASE mensal por (gênero + idade + cobertura)
    """
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
    """
    Fatores (multiplicadores) ajustáveis no Admin.
    Ex:
      - Fumante: SIM = 1.30 / NÃO = 1.00
      - Saúde: Leve = 1.10 / Moderado = 1.25 / Grave = 1.50
    """
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
    """
    Opcional: salvar o pedido no banco (bom para leads).
    """
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