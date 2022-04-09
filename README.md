# Jak włączyć aplikację


## Prerequisites

- python 3.6 installed
- mysql server installed
- mysql client installed

```commandline
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
```

## Requirements for python

- Using pip

```commandline
pip3 install -r requirements.txt
```

- Using Conda

```commandline
conda create --file requirements.yml --name <name>
```

## Run app

```commandline
cd <path_to_app/library>
python manage.py migrate
python manage.py runserver
```

