from django.shortcuts import get_object_or_404
from django.http import Http404


def authenticate_model(model, pk: str):
    try:
        obj = get_object_or_404(model, pk=pk)
    except Http404 as e:
        return Http404(f"Id of {pk} is not valid")

    return obj

