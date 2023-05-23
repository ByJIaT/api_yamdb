# api_yamdb

### Описание

YaMDb — самый популярный и авторитетный в мире источник информации о кино,
телевидении и знаменитостях. Найдите рейтинги и обзоры новейших фильмов и
сериалов.

#### Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с
   параметрами email и username на эндпоинт ```/api/v1/auth/signup/```.
   ```json
   {
     "email": "user@example.com",
     "username": "string"
   }
   ```
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес
   email.
3. Пользователь отправляет POST-запрос с параметрами username и
   confirmation_code на эндпоинт ```/api/v1/auth/token/```, в ответе на запрос
   ему приходит token (JWT-токен).
   ```json
   {
   "username": "string",
   "confirmation_code": "string"
   }
   ```
4. При желании пользователь отправляет PATCH-запрос на
   эндпоинт ```/api/v1/users/me/``` и заполняет поля в своём профайле (описание
   полей — в документации).
   ```json
   {
   "username": "string",
   "email": "user@example.com",
   "first_name": "string",
   "last_name": "string",
   "bio": "string"
   }
   ```

#### Примеры API:

1. Получение списка всех категорий

    ```
    /api/v1/categories/
    ```

    ```json
   {
     "count": 0,
     "next": "string",
     "previous": "string",
     "results": [
       {
         "name": "string",
         "slug": "string"
       }
     ]
   }
    ```

2. Получение списка всех жанров

    ```
    /api/v1/genres/
    ```

    ```json
   {
     "count": 0,
     "next": "string",
     "previous": "string",
     "results": [
       {
         "name": "string",
         "slug": "string"
       }
     ]
   }
   ```

3. Получение списка всех произведений

    ```
    /api/v1/titles/
    ```

    ```json
   {
     "count": 0,
     "next": "string",
     "previous": "string",
     "results": [
       {
         "id": 0,
         "name": "string",
         "year": 0,
         "rating": 0,
         "description": "string",
         "genre": [
           {
             "name": "string",
             "slug": "string"
           }
         ],
         "category": {
           "name": "string",
           "slug": "string"
         }
       }
     ]
   }
    ```
4. Получение списка всех отзывов
    ```
    /api/v1/titles/{title_id}/reviews
    ```

    ```json
   {
     "count": 0,
     "next": "string",
     "previous": "string",
     "results": [
       {
         "id": 0,
         "text": "string",
         "author": "string",
         "score": 1,
         "pub_date": "2019-08-24T14:15:22Z"
       }
     ]
   }
    ```
5. Получение списка всех комментариев к отзыву
    ```
    /api/v1/titles/{title_id}/reviews/{rieviews_id}/comments/
    ```

    ```json
   {
     "count": 0,
     "next": "string",
     "previous": "string",
     "results": [
       {
         "id": 0,
         "text": "string",
         "author": "string",
         "pub_date": "2019-08-24T14:15:22Z"
       }
     ]
   }
    ```

### Технологии

- Python 3.7
- Django 3.2
- DRF 3.12.4

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
https://github.com/ByJIaT/api_yamdb.git
```

```bash
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install -upgrade pip
```

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```

##### Hollywood

### Авторы

- [Булат Габдуллин](https://github.com/ByJIaT) - тимлид команды, описал отзывы (Review) и комментарии (Comments): модели, представления и эндпойнты для них. А также, реализовал систему оценки и рейтинга для произведений.

- [Никита Седымов](https://github.com/JUSTUCKER) - описал категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них. К тому же, разработал management-команду для импорта данных из csv файлов.

- [Камила Беломоина](https://github.com/KamilaBel) - реализовала весь механизм управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном и систему подтверждения через e-mail.
