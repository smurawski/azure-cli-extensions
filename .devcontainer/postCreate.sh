#! usr/local/env bash

git remote add upstream https://github.com/calvinsID/azure-cli-extensions
git fetch upstream containerapp

python -m venv env
source env/bin/activate
python -m pip install -U pip
python -m pip install -U pylint
python -m pip install -U flake8
python -m pip install -U autopep8

pip install azdev
pip install -i https://test.pypi.org/simple/ pycomposefile==0.0.1a1

azdev setup --cli /src/azure-cli --repo .
azdev extension build containerapp
azdev extension build containerapp-preview