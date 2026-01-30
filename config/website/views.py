from django.shortcuts import render

def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def quote(request):
    return render(request, 'website/quote.html')
from django.shortcuts import render

def home(request):
    return render(request, "website/home.html")

def about(request):
    return render(request, "website/about.html")

def plans(request):
    return render(request, "website/plans.html")

def quote(request):
    return render(request, "website/quote.html")

def contact(request):
    return render(request, "website/contact.html")
from django.shortcuts import render
from .models import Banner, HomeCard, GalleryImage

def home(request):
    banners = Banner.objects.filter(is_active=True).order_by("order")
    cards = HomeCard.objects.filter(is_active=True).order_by("order")
    gallery = GalleryImage.objects.filter(is_active=True).order_by("order")
    return render(request, "website/home.html", {
        "banners": banners,
        "cards": cards,
        "gallery": gallery,
    })

def about(request):
    return render(request, "website/about.html")

def plans(request):
    return render(request, "website/plans.html")

def quote(request):
    return render(request, "website/quote.html")

def contact(request):
    return render(request, "website/contact.html")

from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import CoverageAmount, PremiumRate, QuoteFactor, QuoteRequest

def _get_factor(key: str) -> Decimal:
    obj = QuoteFactor.objects.filter(key=key).first()
    return obj.multiplier if obj else Decimal("1.00")


def api_calc_premium(request):
    gender = request.GET.get("gender")
    age = request.GET.get("age")
    coverage_id = request.GET.get("coverage_id")
    smoker = request.GET.get("smoker", "0")
    health = request.GET.get("health", "OK")

    try:
        age = int(age)
        coverage_id = int(coverage_id)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Parâmetros inválidos."}, status=400)

    rate = PremiumRate.objects.filter(gender=gender, age=age, coverage_id=coverage_id).first()
    if not rate:
        return JsonResponse({"ok": False, "error": "Sem preço cadastrado para essa combinação."}, status=404)

    smoker_factor = _get_factor("SMOKER_YES" if smoker == "1" else "SMOKER_NO")

    health_key = {
        "OK": "HEALTH_OK",
        "LIGHT": "HEALTH_LIGHT",
        "MED": "HEALTH_MED",
        "HIGH": "HEALTH_HIGH",
    }.get(health, "HEALTH_OK")
    health_factor = _get_factor(health_key)

    total = (rate.monthly_premium * smoker_factor * health_factor).quantize(Decimal("0.01"))

    return JsonResponse({
        "ok": True,
        "base": str(rate.monthly_premium),
        "smoker_factor": str(smoker_factor),
        "health_factor": str(health_factor),
        "total": str(total),
    })


def quote_page(request):
    coverages = CoverageAmount.objects.all()

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        coverage_id = request.POST.get("coverage_id")
        smoker = request.POST.get("smoker") == "yes"
        health = request.POST.get("health", "OK")
        health_details = request.POST.get("health_details", "").strip()

        try:
            age_int = int(age)
            cov_id = int(coverage_id)
        except (TypeError, ValueError):
            messages.error(request, "Preencha idade e cobertura corretamente.")
            return redirect("/quote/")

        rate = PremiumRate.objects.filter(gender=gender, age=age_int, coverage_id=cov_id).first()
        if not rate:
            messages.error(request, "Não há preço cadastrado para essa combinação. Ajuste no Admin.")
            return redirect("/quote/")

        smoker_factor = _get_factor("SMOKER_YES" if smoker else "SMOKER_NO")
        health_key = {"OK":"HEALTH_OK","LIGHT":"HEALTH_LIGHT","MED":"HEALTH_MED","HIGH":"HEALTH_HIGH"}.get(health, "HEALTH_OK")
        health_factor = _get_factor(health_key)

        total = (rate.monthly_premium * smoker_factor * health_factor).quantize(Decimal("0.01"))

        QuoteRequest.objects.create(
            full_name=full_name,
            email=email,
            gender=gender,
            age=age_int,
            coverage_id=cov_id,
            smoker=smoker,
            health_level=health,
            health_details=health_details,
            calculated_monthly=total,
        )

        messages.success(request, f"Cotação calculada: ${total}/mês. Recebemos seu pedido!")
        return redirect("/quote/")

    return render(request, "website/quote.html", {"coverages": coverages})