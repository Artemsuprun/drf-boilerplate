from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET


# adding a health path to verify that the backend is working
@require_GET
def health(_):
    return JsonResponse({"status": "ok"})
