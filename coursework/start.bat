@echo off
set FLASK_APP=coursework.py
flask db init
flask db migrate
flask db upgrade
