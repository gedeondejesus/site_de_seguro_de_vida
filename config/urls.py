from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def admin_logout_fix(request):
    # Aceita GET e POST
    logout(request)
    return redirect("/admin/login/")

urlpatterns = [
    path("admin/logout/", admin_logout_fix),  # <-- TEM QUE FICAR ANTES DO admin/
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

