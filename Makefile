pip:
	. ./venv/bin/activate; \
	pip install -r requirements.txt; \
	

start:
	. ./venv/bin/activate; \
	foreman start; \
