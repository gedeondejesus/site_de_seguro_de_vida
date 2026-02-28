from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("plans/", views.plans, name="plans"),
    path("contact/", views.contact, name="contact"),
    path("quote/", views.quote_page, name="quote"),

    # ✅ API DO CALCULO
    path("api/calc-premium/", views.api_calc_premium, name="api_calc_premium"),

    # suas 3 páginas
    path("protecao-familiar/", views.protecao_familiar, name="protecao_familiar"),
    path("planejamento-filhos/", views.planejamento_filhos, name="planejamento_filhos"),
    path("estrategia-empresarios/", views.estrategia_empresarios, name="estrategia_empresarios"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)