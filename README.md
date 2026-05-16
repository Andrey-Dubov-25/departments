### Проект Departments

## Описание проекта
Departments - это проект создания подразделений и сотрудников.

Пользователю доступно создание родительских подразделений и стуктурировани дерева от родительского подразделения, создание сотрудников в указанных подразделениях.


**В проекте доступно**:
    создание подразделения;
    создание сотрудника;
    удаления подразделения.


## Используемые технологии
*Проект реализован с использованием следующего функционала*: 
- Python 3.12
- Django 5.1.1 
- Django REST Framework 3.15.2

Все необходимые для работы Departments зависимости перечислены в requirements.txt
Рекомендуется перед установкой развернуть виртуальное окружение с верисей python 3.12:

Bash:
```
py -3.12 -m venv venv 
```

Для установки зависимостей необходимо выполнить команду:
```
pip install -r requirements.txt
```


## Описание API
**API предоставляет следующие возможности:**

- Создание подразделение
- Получение подразделения по id
- Изменение родительского подразделения для наследника
- Удаление подразделения





Возможна фильтрация вывода списка квестов по наличию сотрудников подразделений (?include_employees) и вложенноси подразделений (?depth).

Пример
```
GET /api/departments/1?include_employees=true&depth=4

```



## Примеры запросов API
При локальном запуске проекта документация доступна по адресу:
```
http://localhost/redoc/
```
В документации описаны все доступные эндпоинты, формат запросов, ответов.


**Получение списка всех подразделений**
```
GET /api/departments/

```

```
Content type: application/json

[
    {
        "id": 1,
        "name": "string",
        "employees": [],
        "children": [],
        "created_at": "2026-05-16T09:25:59.994696Z"
    }
]
```

200 - Удачное выполнение запроса  


**Добавление подразделения**

```
POST /api/departments/
```

```
{
"name": "string",
"parent": 1
}
```

201 - Удачное выполнение запроса  
400 - Отсутствует обязательно поле или оно некорректно  


**Удаление подразделения**

```
DELETE /api/departmenrs/{id}/
```

204 - Удачное выполнение запроса  
404 - Подразделение не найден


**Изменить родительское подразделение**

```
PATCH /api/departments/{id}/
```

```
{
    "parent": 2
}
```

200 - Удачное выполнение запроса  
404 - Подразделение не найдено

**Добавить сотрудника**

```
POST /api/quest-types/
```

```
{
    "full_name": "string",
    "position": "string",
    "hired_at": "2019-08-24"
}
```

201 - Удачное выполнение запроса  
400 - Ошибка валидации
404 - Подразделение не найдено


## Команда проекта
Проект создан в качесте тестового задания.  
Над проектом работал [Андрей Дубов](https://github.com/Andrey-Dubov-25)  


## Ссылка на проект
[Проект GQB](https://github.com/Andrey-Dubov-25/departments)

### Как запустить проект:

**Локально**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Andrey-Dubov-25/departments
```

```
cd departments/backend
```


Убедитесь, что DEBUG=True после чего cоздайте и активируйте виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Создать суперпользователя:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

**Через Docker**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Andrey-Dubov-25/departments
```

```
cd departments
```

Запустить контейнеры:

```
docker compose up --build
```

Применить миграции:

```
docker compose exec backend python manage.py migrate
```

Собрать статику:

```
docker compose exec backend python manage.py collectstatic --noinput
```

Скопировать статику в директорию по умолчанию:

```
docker compose exec backend cp -r /app/collected_static/. /backend/static/ 
```


Создать суперпользователя:

```
docker compose exec backend python manage.py createsuperuser
```

**Запуск тестов**

Перед запуском тестов убедитесь, что вы находитесь в корневой директории проекта departments и DEBUG=True, после чего выполните команду:


```
cd backend
```

Запуск тестов на pytest:

```
pytest
```

Запуск flake8:

```
flake8
```