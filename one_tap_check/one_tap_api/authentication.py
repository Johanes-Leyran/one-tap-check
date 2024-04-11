from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Model


def authenticate_model(model, pk: str) -> Model | Exception:
    try:
        obj = get_object_or_404(model, pk=pk)
        return obj
    except model.DoesNotExists:
        raise Http404(f"Invalid ID: {pk}")


def authenticate_each_models(*args: tuple[Model, str]) -> [bool, list[Model | str]]:
    exceptions = []
    models = []
    all_validated = True

    for model, pk in args:
        try:
            res = authenticate_model(model, pk)
            models.append(res)
        except Http404 as e:
            exceptions.append(str(e))

            if all_validated:
                all_validated = False

    # if at least 1 exception present
    if exceptions:
        return all_validated, exceptions

    # if none return the results
    return all_validated, models
