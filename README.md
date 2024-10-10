# Yacut: генерация коротких ссылок
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Mrclive7406/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создайте файл .env c содержимым:

```
FLASK_APP=yacut
FLASK_ENV=development [или production] 
DATABASE_URI=[идентификатор СУБД в формате: mysql://username:password@server/db. опционально, по умолчанию подключится sqlite3]
SECRET_KEY=[ваш случайный ключ]
```

Запуск:

```
flask run
```

Перейдите по url-адресу:
```
[Генерация коротких ссылок](http://127.0.0.1:5000/)
```

## Автор 
- [Колесников Павел ](https://github.com/Mrclive7406)
# GitHub 
- [Проект парсинга pep и документации Python](https://github.com/Mrclive7406/yacut)
