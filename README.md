# todo-do-list-django-practice

This is a Django practice project. Here performed the simplest CRUD operations. You need to only several commands:

## Installation


> 👉 Download the code 

```angular2html
git clone https://github.com/phaishuk/todo-do-list-django-practice
cd todo-do-list-django-practice
```

> 👉 .env file

This project contains some sensitive data, so an `.env` file is required.
Rename the `.env.sample` file to `.env` or create an empty `.env` 
and copy the contents of `.env.sample` there.


> 👉 Install modules via `VENV`  

```angular2html
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on Linux / macOS)
pip install -r requirements.txt
```

> 👉 Set Up Database

```angular2html
python manage.py migrate
```

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

