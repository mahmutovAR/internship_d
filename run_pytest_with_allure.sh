#!/bin/bash

pytest

python3 create_env_properties_file.py

allure generate allure-report --clean --single-file allure-results