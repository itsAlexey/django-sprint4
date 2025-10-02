from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Статичная страница 'О проекте'."""

    template_name = "pages/about.html"


class RulesView(TemplateView):
    """Статичная страница 'Правила'."""

    template_name = "pages/rules.html"


def permission_denied(request, exception):
    """403 ошибка доступа."""
    return render(request, "pages/403.html", status=403)


def csrf_failure(request, reason=""):
    """403 ошибка из-за CSRF."""
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    """404 ошибка."""
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """500 ошибка."""
    return render(request, "pages/500.html", status=500)
