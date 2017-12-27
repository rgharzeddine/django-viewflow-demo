# Django Viewflow Demo

A workflow demo using django, viewflow and adminlte

- [Viewflow](http://viewflow.io/) workflow library
- [Adminlte](https://adminlte.io/) responsive design template

## Requirements

- python 3
- django
- django-viewflow
- celery
- amqp

## Installation

```bash
$ python3 -m venv env
# or
# virtualenv -p python3 env  # python 3.6 tested
$ . env/bin/activate
$ git clone https://github.com/rgharzeddine/django-viewflow-demo.git
$ cd django-viewflow-demo
$ pip install -r requirements.txt

```

## Running Demo

run django
```bash
$ . reset_flows.sh
$ ./manage.py runserver 0.0.0.0:8000

```

run celery worker
```bash
$ celery -A demo worker --loglevel=info

```
