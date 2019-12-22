#!/bin/bash
source venv/bin/activate

echo "Running Pull Request Prep"
export PYTHONPATH=$PWD

echo $PYTHONPATH

echo "Executing black code formatting"
echo " >> see (https://github.com/psf/black)"
black src/
echo -ne '\n'


echo "Executing pylint - python linter"
echo " >> see (https://github.com/PyCQA/pylint)"
pylint src/
echo -ne '\n'


echo "Executing flake8 - python quality/style linter"
echo " >> see (https://github.com/PyCQA/flake8)"
flake8 src/
echo -ne '\n'

echo "Executing pytest - running pytest tests/"

pytest --cov-report term-missing --cov=src/ -vv tests/

echo "Finished!!"