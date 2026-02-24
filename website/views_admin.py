from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

@staff_member_required
def admin_logout_view(request):
    # GET: mostra tela de confirmação
    if request.method == "GET":
        return render(request, "admin/logout.html")

    # POST: faz logout e manda pro login do admin
    logout(request)
    return redirect("/admin/login/")