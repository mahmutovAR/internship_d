#!/bin/bash

#pytest -n 5 --disable-warnings --alluredir=allure-results --clean-alluredir
pytest tests/test_request_get_post.py

#python3 create_env_properties_file.py

#allure generate allure-report --clean --single-file allure-results