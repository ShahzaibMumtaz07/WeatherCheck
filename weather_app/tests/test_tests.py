from http import HTTPStatus
from django.core.cache import cache
from django.test import TestCase
from django.conf import settings
from weather_app.forms import InputForm
from weather_app.utils import THIRD_PARTY_API_URL, THIRD_PARTY_RESPONSES
from django.urls import reverse


class InputFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.API_KEY = settings.API_KEY
        cls.index_url = reverse("weather_app:index")

    def test_successful(self):
        city = "Karachi"
        lang = "en"
        form = InputForm(data={"city": city})
        self.assertEqual(form.is_valid(),True)
        resp = form.search_the_city("en")
        self.assertEqual(resp.get('city'), city)
        self.assertEqual(resp.get('success'), True)
        cache_resp = cache.get("*".join([city, lang]))
        self.assertEqual(cache_resp.get('city'),city)
        self.assertEqual(cache_resp.get('success'),True)

    def test_unsuccessful(self):
        city = "Abcde"
        lang = "fr"
        exp_result = {
            "city": city,
            **THIRD_PARTY_RESPONSES.get(HTTPStatus.NOT_FOUND)
        }
        form = InputForm(data={"city": city})
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.search_the_city(lang), exp_result)

    def test_index_page(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,'<i class="fas fa-search">')
        
    def test_post_form_via_view(self):
        city = "Karachi"
        response = self.client.post(self.index_url, {"city": city})
        self.assertContains(response, '<li class="list-group-item d-flex justify-content-between align-items-center">Temperature')

    def test_cache(self):
        exp_value = "foo"
        city = "Amsterdam"
        lang = "de"
        cache.set("*".join([city, lang]), exp_value)
        form = InputForm(data={"city": city})
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.search_the_city(lang),exp_value)