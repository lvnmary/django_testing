# Django testing
#### Тестирование проектов YaNote и YaNews на unittest и pytest соответственно. Django-проект YaNews: новостной сайт, где пользователи могут оставлять комментарии к новостям. Django-проект YaNote: электронная записная книжка для тех, кто не хочет ничего забыть и поэтому всё записывает.
## Структура репозитория:
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```
## Для проверки тестов:
1. Создать и активировать виртуальное окружение; 
2. Установить зависимости из файла `requirements.txt`;
3. Запустить скрипт для `run_tests.sh` из корневой директории проекта: `bash run_tests.sh`.