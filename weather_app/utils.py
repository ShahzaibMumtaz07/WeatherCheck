from django.utils.translation import ugettext_lazy as _
from http import HTTPStatus

def calc_direction_and_parse_json(response):
    """
    Calculating wind direction and parsing response json
    """

    wind_deg = response.get("wind").get("deg")
    val=int((wind_deg/22.5)+.5)
    arr=[_(x) for x in ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]]
    wind_dir = arr[(val % 16)]
    

    return {
        "desc": response["weather"][0]["description"].strip().title(),
        "icon": response["weather"][0]["icon"],
        "temp": response["main"]["temp"],
        "temp_min": response["main"]["temp_min"],
        "temp_max": response["main"]["temp_max"],
        "humidity": response["main"]["humidity"],
        "pressure": response["main"]["pressure"],
        "wind_speed": response["wind"]["speed"],
        "wind_direction": wind_dir,
    }

THIRD_PARTY_API_URL = "https://api.openweathermap.org/data/2.5/weather"

THIRD_PARTY_RESPONSES = {
    HTTPStatus.OK: {
        "success": True
    },
    HTTPStatus.BAD_REQUEST: {
        "success": False,
        "error": _("Invalid syntax"),
    },
    HTTPStatus.UNAUTHORIZED: {
        "success": False,
        "error": _("Invalid API key"),
    },
    HTTPStatus.REQUEST_TIMEOUT: {
        "success": False,
        "error": _("API not working at the current moment."),
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        "success": False,
        "error": _("Internal Server Error"),
    },
    HTTPStatus.NOT_FOUND: {
        "success": False,
        "error": _("City not found"),
    },   
}
