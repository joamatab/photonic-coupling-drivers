
install: 
	pip install -r requirements.txt --upgrade
	pip install -r requirements_dev.txt --upgrade
	pip install -e .
	pre-commit install

test:
	pytest

cov:
	pytest --cov= plab

mypy:
	mypy . --ignore-missing-imports

lint:
	flake8 

pylint:
	pylint plab

lintd2:
	flake8 --select RST

lintd:
	pydocstyle plab

doc8:
	doc8 docs/
