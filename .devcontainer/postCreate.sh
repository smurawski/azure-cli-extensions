python -m venv env
source env/bin/activate
python -m pip install -U pip

pip install azdev
pip install pycomposefile

azdev setup --repo .
azdev extension build containerapp
azdev extension build containerapp-compose
