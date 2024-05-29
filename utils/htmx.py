import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response


def render_toast_message(title, message, level="info"):
    level = level.lower()
    event_details = {
        "show-toast": {"level": level, "title": title, "message": message}
    }
    response = HttpResponse(status=status.HTTP_204_NO_CONTENT)
    response["HX-Trigger"] = json.dumps(event_details)
    return response


def render_toast_message_for_api(title, message, level="info"):
    level = level.lower()
    event_details = {
        "show-toast": {"level": level, "title": title, "message": message}
    }
    response = Response({"success": True})
    response.headers["HX-Trigger"] = json.dumps(event_details)
    return response
