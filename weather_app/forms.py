from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.cache import cache
from django.conf import settings

import requests
from .utils import calc_direction_and_parse_json, THIRD_PARTY_API_URL,THIRD_PARTY_RESPONSES

class InputForm(forms.Form):
    city = forms.CharField(max_length=128, label=_("City Name"))

    @staticmethod
    def call_third_party(city, lang):
        """
        Calling third-party service for weather update.
        :param city : incoming city name
        :param lang : incoming current language from view
        :return:
            {
                "success": bool,
                "city": str,  
                "error": str
            }
        """

        response = requests.get(THIRD_PARTY_API_URL,params={
                "q": city,
                "appid": settings.API_KEY,
                "lang": lang,
                "units": "metric",
            }
        )

        resp_message = THIRD_PARTY_RESPONSES.get(
            response.status_code,
            {
                "success": False,
                "error": _("Unhandled exception"),
            },
        )
        resp_message["city"] = city

        if resp_message.get("success", None):
            resp_message.update(calc_direction_and_parse_json(response.json()))

        return resp_message

    def search_the_city(self, lang):
        """
        Hit the cache for reqeust else call the third party
        :param lang: incoming current language from views for third-party call
        :return:
            2xx:
                {
                    "success": bool,
                    "result": dict,
                    "error": empty
                }

            3xx,4xx.5xx:
                {
                    "success": bool,
                    "result": empty,
                    "error": str
                }
        """
        city = self.cleaned_data.get('city').strip().title()

        cache_key = "*".join([city, lang])
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        else:
            result = self.call_third_party(city, lang=lang)
            cache.set(cache_key, result, settings.CACHE_TIMEOUT)
            return result
