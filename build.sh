#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
cd instituto_recuay
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py crear_superadmin
