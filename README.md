# Star wars API

## Postman Collection
  https://elements.getpostman.com/redirect?entityId=24358209-d121d8de-3e9f-4290-88a4-bb55dc733f92&entityType=collection
  
  Additionally you can visit http://127.0.0.1:8000/api/v1/docs/ for swagger UI

## _Installation and setup process_

## Manual

### Requirements

1. [PostgreSQL](https://www.postgresql.org/download/)
2. [Poetry](https://python-poetry.org/docs/)

### How to run it?

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
$ git clone https://github.com/ankitsagar/star_wars.git
```

3. Go to the cloned directory:
```
$ cd star_wars
```

3. Install the dependencies:
```
$ poetry install
```

4. Activate virtual env:
```
$ source $(poetry env info --path)/bin/activate
```
  For fish shell
```
$ source $(poetry env info --path)/bin/activate.fish
```

5. Go to app folder:
```
$ cd star_wars
```

6. Run migrations:
```
$ python manage.py migrate
```

7. Populate all required data to db:
```
$ python manage.py load_data
$ python manage.py loaddata users
```

8. Run the app:
```
$ python manage.py runserver
```

*App will be available on port 8000*

9. Run test:
```
$ python manage.py test
```

## With Docker

### Requirements
1. [Docker](https://docs.docker.com/install/)
2. [Docker Compose](https://docs.docker.com/compose/install/)

### How to run it?

1. Clone the repository:
```
$ git clone https://github.com/ankitsagar/star_wars.git
```

2. I am using shared folders to enable live code reloading. Without this, Docker Compose will not start:
    - Windows/MacOS: Add the cloned `star_wars` directory to Docker shared directories (Preferences -> Resources -> File sharing).
    - Windows/MacOS: Make sure that in Docker preferences you have dedicated at least 1 GB of memory (Preferences -> Resources -> Advanced).
    - Linux: No action required, sharing already enabled and memory for Docker engine is not limited.

3. Go to the cloned directory:
```
$ cd star_wars
```
4. Build the application:
```
$ docker-compose build
```
5. Run the application:
```
$ docker-compose up
```
*All the components might take up to few minutes for them to compile depending on your CPU, After it's done app will be available on port 8000*
