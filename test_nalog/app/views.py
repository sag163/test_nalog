from django.shortcuts import render

from selenium import webdriver
from bs4 import BeautifulSoup
from .forms import InnForm
from django.http import HttpResponse
from .models import Nalog


from time import sleep
from .cache import cache_func
from django.views.generic import View





def get_html(search_number):
    chromedriver = "/home/sag163/Документы/project/nalog/test_nalog/app/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    browser.get("https://rmsp.nalog.ru/")
    search = browser.find_element_by_xpath('//*[@id="query"]')
    search.send_keys(search_number)
    search.submit()
    sleep(3)
    html = browser.page_source
    return html


@cache_func
def get_content(search_number):
    html = get_html(search_number)
    soup = BeautifulSoup(html, "html5lib")
    items = soup.find_all("div", {"class": "result-name"})
    if items and len(items) == 1:
        return True
    else:
        return False


def inn_or_ogrn(number):
    """ Функция проверяет подлинность номера ИНН/ОГРН"""
    number = str(number)
    len_number = len(number)
    if len_number == 13:
        # Проверяем соответствие требованиям шифра ОГРН
        a = number[:12]
        b = number[-1]
        if int(a) % 11 == int(b):
            return "ОГРН"
    elif len_number == 10:
        # Проверяем соответствие требованиям шифра ИНН (10знаков)
        control_count = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum = 0
        for i in range(9):
            control_sum += control_count[i] * int(number[i])
        result = control_sum % 11
        if result == 10:
            result = 0
        elif result > 9:
            result = control_sum % 10
        if result == int(number[-1]):
            return "ИНН"
    elif len_number == 12:
        # Проверяем соответствие требованиям шифра ИНН (12знаков)
        # Вычисляем 1-е контрольное число
        control_count = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
        control_sum = 0
        for i in range(11):
            control_sum += control_count[i] * int(number[i])
        result = control_sum % 11
        if result == 10:
            result = 0
        elif result > 9:
            result = control_sum % 10
        # Вычисляем 2-е контрольное число
        control_count_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum_2 = 0
        for i in range(11):
            control_sum_2 += control_count_2[i] * int(number[i])
        result_2 = control_sum_2 % 11
        if result_2 == 10:
            result_2 = 0
        elif result_2 > 9:
            result_2 = control_sum % 10
        if result == int(number[-2]) and result_2 == int(number[-1]):
            return "ИНН"


class Index(View):
    def get(self, request):
        nalog_form = InnForm()
        result = Nalog.objects.all
        return render(request, "index.html", {"result": result, "form": nalog_form})

    def post(self, request):

        result_true = "True"
        result_false = "False"
        nalog_form = InnForm(request.POST or None)
        number = request.POST.dict()["request_numbers"]
        check_inn_ogrn = inn_or_ogrn(number)
        if check_inn_ogrn not in ["ИНН", "ОГРН"]:
            return HttpResponse("Проверьте введеные значения")
        answer = get_content(number)
        inn_ogrn = inn_or_ogrn(number)
        if answer:
            Nalog.objects.create(request_numbers=number, answer=result_true)
            return HttpResponse(result_true)
        else:
            Nalog.objects.create(request_numbers=number, answer=result_false)
            return HttpResponse(result_false)
