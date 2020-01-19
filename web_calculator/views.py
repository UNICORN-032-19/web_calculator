from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .calculator.calc import Calculator, UnknownOperation, UnknownError
import json
from web_calculator.common.models import Result

calc = Calculator(start_auto=False)


def get_result(string):
    result = "0"
    error = ""
    elements = calc.prepare_data(string)
    try:
        result = calc.calc(elements)
    except ZeroDivisionError:
        error = "На ноль делить нельзя!"
    except UnknownOperation as error:
        error = "UnknownOperation"
    except UnknownError:
        error = "UnknownError!"
    return str(result), str(error)

def home(request):
    return render(request, 'home.html')

def compute(request):
    return_result = dict(
        string="0",
        error="",
    )
    string = request.POST.get("string", "").strip()
    if string.endswith("="):
        string = string.replace("=", "")
        result, error = get_result(string)
        if error:
            return_result.update({"error": error})
        else:
            return_result.update({"string": result})
    elif string.endswith("X^2"):
        string = string[:-3]
        error = ""
        try:
            float(string)
            result1 = string
        except ValueError:
            result1, error = get_result(string)

        try:
            if error:
                raise ValueError(error)
            result, error = get_result(result1 + "^2")
            if error:
               raise ValueError(error)
            return_result.update({"string": result})
        except ValueError as error:
            return_result.update({"error": error})
    else:
        return_result.update({"string": string})
    Result.objects.create(string=string, result=return_result.get("string"), error=return_result.get("error"))
    return HttpResponse(json.dumps(return_result), content_type="text/json")

def results(request):
    results = Result.objects.all()
    return render(request, 'results.html', context={"results": results})
