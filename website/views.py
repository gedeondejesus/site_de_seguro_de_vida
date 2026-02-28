import re
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Audience

from django.shortcuts import get_object_or_404






def audience_detail(request, slug):
    audience = get_object_or_404(Audience, slug=slug)
    return render(request, "website/audience_detail.html", {
        "audience": audience
    })



import logging
logger = logging.getLogger(__name__)

def quote(request):
    logger.warning("QUOTE VIEW: method=%s", request.method)
    if request.method == "POST":
        logger.warning("QUOTE POST DATA: %s", dict(request.POST))
    




from .models import (
    Banner, HomeCard, GalleryImage,
    Testimonial, VideoTestimonial,
    TermRate
)


# =========================
# HELPERS
# =========================
def _to_bool(v):
    return str(v).strip().lower() in ("1", "true", "yes", "sim", "on")


def _to_int(v):
    s = re.sub(r"[^\d]", "", str(v or ""))
    return int(s) if s else None


# =========================
# HOME
# =========================
def home(request):
    banners = Banner.objects.filter(is_active=True).order_by("order")
    cards = HomeCard.objects.filter(is_active=True).order_by("order")
    gallery = GalleryImage.objects.filter(is_active=True).order_by("order")

    testimonials = Testimonial.objects.filter(
        is_active=True,
        allow_publish=True,
        is_approved=True
    ).order_by("-created_at")[:6]

    video_testimonials = VideoTestimonial.objects.filter(
        is_active=True,
        allow_publish=True,
        is_approved=True
    ).order_by("order", "-created_at")[:6]

    audiences = Audience.objects.filter(is_active=True).order_by("order", "id")

    return render(request, "website/home.html", {
        "banners": banners,
        "cards": cards,
        "gallery": gallery,
        "gallery_images": gallery,
        "testimonials": testimonials,
        "video_testimonials": video_testimonials,
        "audiences": audiences,
    })

def about(request):
    return render(request, "website/about.html")


def plans(request):
    return render(request, "website/plans.html")


# =========================
# API: CÁLCULO DO PRÊMIO
# /api/calc-premium/?gender=F&age=35&coverage=300000&smoker=1&health=OK
# =========================
def api_calc_premium(request):
    gender = (request.GET.get("gender") or "").strip().upper()
    age = _to_int(request.GET.get("age"))
    coverage = _to_int(request.GET.get("coverage"))
    smoker = _to_bool(request.GET.get("smoker"))
    health = (request.GET.get("health") or "OK").strip().upper()

    if gender not in ("M", "F") or age is None or coverage is None:
        return JsonResponse({"ok": False, "error": "Dados inválidos."}, status=400)

    rate = TermRate.objects.filter(
        gender=gender,
        age=age,
        coverage=coverage,
        smoker=smoker,
    ).first()

    if not rate:
        return JsonResponse(
            {"ok": False, "error": "Sem preço cadastrado para essa combinação."},
            status=404
        )

    base = Decimal(str(rate.price))

    health_factor = {
        "OK": Decimal("1.00"),
        "LIGHT": Decimal("1.15"),
        "MED": Decimal("1.35"),
        "HIGH": Decimal("1.70"),
    }.get(health, Decimal("1.00"))

    total = (base * health_factor).quantize(Decimal("0.01"))
    return JsonResponse({"ok": True, "price": float(total)})


# =========================
# QUOTE PAGE (FORM + EMAIL)
# =========================
def quote_page(request):
    coverages = [300000, 500000, 700000, 1000000]

    if request.method == "POST":
        full_name = (request.POST.get("full_name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        gender = (request.POST.get("gender") or "").strip().upper()

        age = _to_int(request.POST.get("age"))
        coverage = _to_int(request.POST.get("coverage"))
        smoker = _to_bool(request.POST.get("smoker"))
        health = (request.POST.get("health") or "OK").strip().upper()
        health_details = (request.POST.get("health_details") or "").strip()

        if gender not in ("M", "F") or age is None or coverage is None:
            messages.error(request, "Preencha idade, gênero e cobertura corretamente.")
            return redirect("/quote/")

        rate = TermRate.objects.filter(
            gender=gender,
            age=age,
            coverage=coverage,
            smoker=smoker,
        ).first()

        monthly_value = rate.price if rate else None

        subject = "New Quote Request - Heller Finance"
        to_email = ["hellerfinance5r@gmail.com"]

        body = f"""
New quote request received:

Full Name: {full_name}
Email: {email}
Phone: {phone}

Gender: {gender}
Age: {age}
Coverage: {coverage}
Smoker: {"YES" if smoker else "NO"}
Health: {health}
Health Details: {health_details}

Estimated Monthly: {monthly_value if monthly_value is not None else "NOT FOUND (check rate table)"}
        """.strip()

        try:
            msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_email,
                reply_to=[email] if email else None,
            )
            msg.send(fail_silently=False)
            messages.success(request, "Sua solicitação foi enviada com sucesso! Em breve entraremos em contato.")
        except Exception as e:
            messages.error(request, f"Não foi possível enviar agora. (Erro: {str(e)})")

        return redirect("/quote/")

    return render(request, "website/quote.html", {"coverages": coverages})


def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message = (request.POST.get("message") or "").strip()

        subject = "New Contact Message - Heller Finance"
        to_email = ["hellerfinance5r@gmail.com"]

        body = f"""
New message from Contact page:

Name: {name}
Email: {email}

Message:
{message}
        """.strip()

        try:
            msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_email,
                reply_to=[email] if email else None,
            )
            msg.send(fail_silently=False)
            messages.success(request, "Mensagem enviada com sucesso! Em breve entraremos em contato.")
        except Exception as e:
            messages.error(request, f"Não foi possível enviar a mensagem agora. (Erro: {str(e)})")

        return redirect("/contact/")

    return render(request, "website/contact.html")
def protecao_familiar(request):
    return render(request, "website/protecao_familiar.html")


def planejamento_filhos(request):
    return render(request, "website/planejamento_filhos.html")


def estrategia_empresarios(request):
    return render(request, "website/estrategia_empresarios.html")


def protecao_familiar(request):
    return render(request, "website/protecao_familiar.html")

def planejamento_filhos(request):
    return render(request, "website/planejamento_filhos.html")

def estrategia_empresarios(request):
    return render(request, "website/estrategia_empresarios.html")