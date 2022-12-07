from django.shortcuts import render
from .forms import InputForm
from django.utils.translation import get_language


def index(request):
    current_language = get_language()
    form = InputForm(request.POST or None)
    resp_data = {}
    if form.is_valid():
        resp_data = form.search_the_city(lang=current_language)
    return render(request, "index.html", {"form": form, **resp_data})