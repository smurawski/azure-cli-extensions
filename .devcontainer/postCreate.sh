#! usr/local/env bash

git remote add upstream https://github.com/calvinsID/azure-cli-extensions
git fetch upstream containerapp

python -m venv env
source env/bin/activate
pip install -U pip
pip install -U pylint
pip install -U flake8
pip install -U autopep8

pip install -U azdev
pip install -U pycomposefile

azdev setup --cli /src/azure-cli --repo .
azdev extension build containerapp
azdev extension build containerapp-preview

az provider register -n Microsoft.App --wait
