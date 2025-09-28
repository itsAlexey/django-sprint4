from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """О проекте."""

    template_name = "pages/about.html"


class RulesView(TemplateView):
    """Правила использования."""

    template_name = "pages/rules.html"

def permission_denied(request, exception):
    """Ошибка 403 (нет прав)."""
    return render(request, "pages/403.html", status=403)


def csrf_failure(request, reason=""):
    """Ошибка 403 CSRF."""
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    """Ошибка 404."""
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """Ошибка 500."""
    return render(request, "pages/500.html", status=500)