# Pet Shop
## Installing guid:

#### Pet shop task requires [Python](https://www.python.org/) v3.8.6+ to run perfectly.
Install python version ‘3.8.6’ from [python-download-v3.8.6](https://www.python.org/downloads/release/python-386/) then add the path to “Environment Variables”.

Create a virtual environment:

```sh
python -m venv venv (windows)
python3 -m venv venv (ubunto/linux)
```

Activate the virtual environment:

```sh
source venv/Scripts/activate (windows)
source venv/bin/activate (ubunto/linux)
```
Install requirement packages for the project:

```sh
pip install -r requirement.txt
```
Make migration files:

```sh
python manage.py makemigrations
```

Migrate the tables:

```sh
python manage.py migrate
```
Create a superuser:

```sh
python manage.py createsuperuser
```
Load the fixtures(database dumps) into database:

```sh
python manage.py loaddata db.json
```
Finally, runserver:

```sh
python manage.py runserver
```
