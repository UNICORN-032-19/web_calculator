from django.shortcuts import render, redirect
from datetime import datetime
from .calculator.calc import Calculator, UnknownOperation, UnknownError

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
    string = request.GET.get("string", "").strip()
    to_error = request.GET.get("error", "").strip()
    string = string.replace("plus", "+")
    if string.endswith("equal"):
        string = string.replace("equal", "")
        result, error = get_result(string)
        if error:
            return redirect(request.path + "?" + "error=" + error)
        else:
            return redirect(request.path + "?" + "string=" + result)
    if string.endswith("C"):
        return redirect(request.path + "?" + "string=0")
    if string.endswith("DEL"):
        return redirect(request.path + "?" + "string=" + string[:-4])
    if string.startswith("0"):
        return redirect(request.path + "?" + "string=" + string[1:])
    if string.endswith("X^2"):
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
            return redirect(request.path + "?" + "string=" + result)
        except ValueError as error:
            return redirect(request.path + "?" + "error=" + error)

    if not string:
        string = "0"
    context = {'timestamp': datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"), 'string': string, 'to_error': to_error}
    return render(request, 'home.html', context)

def compute(request):
    pass
