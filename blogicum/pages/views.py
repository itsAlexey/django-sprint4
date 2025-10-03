from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Статическая страница «О проекте»."""

    template_name = "pages/about.html"


class Rules(TemplateView):
    """Статическая страница «Правила»."""

    template_name = "pages/rules.html"


def _render_error(template, status_code, request):
    """Универсальный рендер ошибок."""
    return render(request, template, status=status_code)


def page_not_found(request, exception):
    """Обработка 404 — страница не найдена."""
    return _render_error("pages/404.html", 404, request)


def csrf_failure(request, reason=""):
    """Обработка 403 при ошибке проверки CSRF."""
    return _render_error("pages/403csrf.html", 403, request)


def server_error(request):
    """Обработка 500 — внутренняя ошибка сервера."""
    return _render_error("pages/500.html", 500, request)
