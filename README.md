### Описание проекта 

Проект YaMDb собирает отзывы пользователей на произведения (фильмы, книги, музыка). Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 

### Авторы 

Студенты 57 когорты Яндекс Практикума по направлению "Python-разработчик":
Александр Бойко, Евгений Чичин, Евгения Полякова.

### Стек технологий: 

Python, Django, Django Rest Framework, API 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

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

Запустить проект:

```
python manage.py runserver 
``` 
### Как создать администратора: 

```
python manage.py createsuperuser
```  

Далее придумайте логин и пароль, если пароль будет очень лёгким, Django предложит усложнить его. 

### Примеры запросов к API:  

1.Post. Добавление новой категории. Права доступа: Администратор.  
``` 
 api/v1/categories/ 
```

```
{
    "name": "string",
    "slug": "string"
}
```
Пример успешного ответа:
```
{
    "name": "string",
    "slug": "string"
}
```
2. Get. Получение списка всех жанров. Права доступа: Доступно без токена. 
```
`api/v1/genre/`
``` 

Пример успешного ответа:
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
]
```
3. Post. Добавление произведения. Права доступа: Администратор.
```  
api/v1/titles/ 
```

```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
Пример успешного ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
``` 

### Команда для запуска скрипта по загрузке данных из csv файлов: 
``` 
python manage.py import_files 
``` 

### Докуметация для API YaMDb:

Запустите проект и перейдите по адресу: 

```
http://127.0.0.1:8000/redoc/
```