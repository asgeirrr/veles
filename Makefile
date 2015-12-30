SHELL = bash

VIRTUAL_ENV = venv
LOCALPATH = $(CURDIR)
PYTHONPATH = $(LOCALPATH)/$(DJANGO_DIR)
JS_DIR = $(LOCALPATH)/static/js

pip:
	. ./venv/bin/activate; \
	pip install -r requirements.txt; \
	

start:
	. ./venv/bin/activate; \
	foreman start; \

runserver:
	. ./venv/bin/activate; \
	./manage.py runserver

showurls:
	. ./venv/bin/activate; \
	./manage.py show_urls

resetdb:
	. ./venv/bin/activate; \
	./manage.py reset_db --noinput
	./manage.py syncdb --noinput