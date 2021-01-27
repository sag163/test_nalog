Перед вами програма проверяет, является ли переданный ОГРН или ИНН субъектом малого или среднего предпринимательства на сайте https://rmsp.nalog.ru/. На главной странице результаты предыдущих проверок.

Инструкция по запуску проекта:  

1. Создадим виртуальное окуржение:
    python3 -m venv venv


2. Активировать виртуальное окружение (для Linux):
    source venv/bin/activate

3. Установить Джанго:
    pip install -r requirements.txt

4. Из папки в которой находится файл manage.py выполнить миграции:
    python3 manage.py migrate

5. И запустить проект:
    python3 manage.py runserver

