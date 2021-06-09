# Pet Shop
## Pet Shop where you can Create, Review, Update, Delete and Order your favourite pets with different prices and currencies.

### Installing guid:

#### Pet shop task requires [Python](https://www.python.org/) v3.8.6+ to run perfectly.
Install python version ‘3.8.6’ from [python-download-v3.8.6](https://www.python.org/downloads/release/python-386/) then add the path to “Environment Variables”.

Create a virtual environment called 'venv':

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
Create a superuser to view data from django admin panel:

```sh
python manage.py createsuperuser
```
Finally, runserver:

```sh
python manage.py runserver
```
To run coverage test:

```sh
coverage run manage.py test pet
```
To render coverage test as html page:

```sh
coverage html
```
Open `'Project_Dir'/html/index.html` then filter by app_name `pet`.