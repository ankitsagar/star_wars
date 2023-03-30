# Star wars API

## Postman Collection
  https://elements.getpostman.com/redirect?entityId=24358209-d121d8de-3e9f-4290-88a4-bb55dc733f92&entityType=collection

## _Installation and setup process_

## Requirements

1. [PostgreSQL](https://www.postgresql.org/download/)
2. [Poetry](https://python-poetry.org/docs/)

## How to run it?

1. Create a database and user:
```
sudo -u postgres psql
postgres=# create database star_wars;
postgres=# create user choosen_one with encrypted password 'last_jedi';
postgres=# grant all privileges on database star_wars to choosen_one;
```
If you want to run test cases (Optional)
```
postgres=# ALTER USER choosen_one CREATEDB;
```

2. Clone the repository:
```
$ https://github.com/ankitsagar/star_wars.git
```

3. Go to the cloned directory:
```
$ cd star_wars
```

3. Install the dependencies:
```
$ poetry install
```

4. Go to app folder:
```
$ cd star_wars
```

4. Run the app:

```
$ python manage.py runserver
```

*App will be available on port 8000*

4. Run test:

```
$ python manage.py test
```
