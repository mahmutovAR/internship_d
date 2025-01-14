#!/bin/bash

pytest -n 4 --disable-warnings --alluredir=allure-results --clean-alluredir

python3 create_env_properties_file.py

allure generate allure-report --clean --single-file allure-results